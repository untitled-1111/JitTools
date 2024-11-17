# Side effect tracing

Note: Read about the slot finder first. Otherwise this won't
make a lot of sense.

Note 2: Not currently implemented. Update with the commit ID one done.

This is the problem of slot elimination changing the behaviour
of the program by reordering observable events (actions with
side effects). Take, for example, this simple program:

```lua
local prev = get_myvar()
set_myvar(123)
print(prev)
```

With standard slot elimination, this is decompiled to:

```lua
set_myvar(123)
print(get_myvar())
```

... which obviously has very different behaviour. While that was
a very obvious example, there are also more subtle examples that
usually don't make any difference. This for example:

```lua
local a = f()
print(a)

-- Pseudocode:
slot0 = f
slot0 = f()
slot1 = print
slot1(slot0)
```

decompiles to:

```lua
print(f())

-- Pseudocode:
slot0 = print
slot1 = f
slot1 = slot1()
slot0(slot1)
```

This might not seem like it makes any difference, but if you have a
metatable set on `_G`, then you can see the order the reads are made
in. Also (this being the reason why I'm currently working on this) the
difference impacts the bytecode when you recompile a program, and hence
it prevents the old tests from matching.

A seemingly simple solution is to avoid inlining across observable
actions (henceforth OA) - if an OA appears between when a slot is set
and when it's used, the inline is blocked. That is very simple to
implement, but is too aggressive. This:

```lua
f(x, y, z)
```

Decompiles to:

```lua
local slot0 = f
local slot1 = x
local slot2 = y
slot0(slot1, slot2, z)
```

since all but the last global reference are blocked by the OA of
reading `z`. This would be correct if LuaJIT evaluated the arguments
in random order, but it doesn't - first the function expression (`slot0` here)
is evaluated, followed by each argument in order. This means we can
inline the other three slots without changing the program meaning.

One potential solution is to run slotworks over and over again - if we
ran slotworks again over the previous program it'd inline `slot2` (since
slot3 is gone) and so on until it stopped changing. This would work, but
would most likely be unacceptably slow (and performance is something I'd
like to improve over time, especially when decompiling large codebases
and running the tests).

## Proposed solution

The current plan is to track the assignments between the slot's assignment
and it's first use. If we find an OA in that period that's not inside
an assignment, skip it since we can't inline it.

We should then iterate backwards over the slots during elimination. If
all the assignments between the assignment and use have been eliminated
then we can safely inline it without making further passes.

For example, starting at the following:

```lua
slot0 = f -- Assn List: slot1, slot2, slot3
slot1 = x -- Assn List: slot2, slot3
slot2 = y -- Assn List: slot3
slot3 = z -- Assn List: empty
slot0(slot1, slot2, slot3)
```

Then during slot elimination, first eliminate the last slot:

```lua
slot0 = f -- Assn List: slot1, slot2, slot3 -- Unsafe, slot1 and slot2 remaining
slot1 = x -- Assn List: slot2, slot3 -- Unsafe, slot2 remaining
slot2 = y -- Assn List: slot3 -- Safe to inline, slot3 is eliminated
slot0(slot1, slot2, z)
```

Going to the next slot, we can now eliminate `slot2` since the only assignment
between it's assignment and it's usage (`slot3`) has been eliminated (this is
very quick to check via `_is_invalidated`, since we tag eliminated assignments).

## Slot-to-slot assignments

(note: this is specifically an implementation detail, and doesn't change the
overall solution detailed above)

One problem here is slot-to-slot assignments, since they allow the slot eliminator
to work on earlier (in the program) slots after they've been used, and swap them
in after all the assignments in the way have been eliminated.

Take for example:

```lua
slot0 = f1()
slot1 = f2()
slot2 = slot0
print(slot1, slot2)
```

(For now I'll assume that `print` is a local for the sake of discussion)

Could end up as `print(f2(),f1())` and execute the functions in the wrong order - since
the slots are walked backwards, first slot2 will be eliminated, then slot1 will be
eliminated - nothing wrong yet. The problem is when slot0 is eliminated - since the
assignment to slot1 has been eliminated previously, it'll consider it safe to merge
in slot0.

The solution is to assign serial numbers to each assignment as they are eliminated. When
we eliminate a slot that references another slot, tag the source slot (in the example
above, `slot0`) with the current serial. When that slot is eliminated, don't cross eliminated
assignments with a greater serial.

Thus when the earlier (in the program) slot is eliminated, it'll try and cross the
assignments that were eliminated later (decompile order) and thus have a greater serial. The
elimination will then be cancelled.

This allows the following code to still work:

```lua
slot0 = f1()
slot2 = f2()
slot1 = slot0
print(slot1, slot2)
```

(NOTE: The above won't decompile correctly and slot0 will become a local variable. I'm
writing this long after I wrote the main body of this part, and the issue is the difference
between the argument order and assignment order. If you eliminated slots right-to-left as
they appear in the arguments list it'll work. AFAIK this shouldn't be an issue, since
(again, afaik) LuaJIT writes the arguments to the stack in assignment order. However there
is the potential here for stuff to be incorrectly inlined or not inlined here if LuaJIT
does something unexpected.)

Allow slot-to-slot assignments to be inlined regardless of side effect tracking, since
otherwise the following would end up with an extra local variable in the output:

```lua
slot0 = f3() -- slot0 has been tagged, can't inline past slot1
slot1 = f1() -- Gets inlined
slot2 = slot0 -- slot2 has been tagged and can't inline past slot3
slot3 = f2() -- Gets inlined
slot4 = slot2 -- Gets inlined, tags slot2
slot5 = f4() -- Gets inlined
print(slot1, slot3, slot4, slot5)
```

This "don't inline past" serial has to be propagated across slot-to-slot assignments
though to avoid this collapsing:

```lua
slot0 = f1() -- slot0 has been tagged late from the previous assignment, inlines
slot2 = slot0 -- inlined since slot-to-slot inlines are allowed, see above
slot1 = f2()
slot3 = slot2 -- slot2 is tagged
print(slot1, slot3)
```
