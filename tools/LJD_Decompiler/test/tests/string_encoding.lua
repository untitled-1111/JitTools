-- Check that the decompiler doesn't get strings wrong if they use hex
-- encoding or non-ASCII characters.

-- Latin-1 and non-Latin-1 text
f("Hello, World!")
f("Привет, Мир!")

-- Hex codes to insert arbitary bytes
f("\x00\x01\x02\x03Hi") -- All low, not UTF-8 specials
f("a\xc7b") -- Can it recover?
f("a\xb9b") -- UTF-8 entry claiming to be one byte long
f("a\xc7") -- Ending mid-codepoint
