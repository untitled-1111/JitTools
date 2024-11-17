local vkeys = require("vkeys")
local imgui = require("imgui")
local wm = require("lib.windows.message")

vkeys.key_names[vkeys.VK_LMENU] = "L Alt"
vkeys.key_names[vkeys.VK_RMENU] = "R Alt"
vkeys.key_names[vkeys.VK_LSHIFT] = "L Shift"
vkeys.key_names[vkeys.VK_RSHIFT] = "R Shift"
vkeys.key_names[vkeys.VK_LCONTROL] = "L Ctrl"
vkeys.key_names[vkeys.VK_RCONTROL] = "R Ctrl"

local list = {}
local module = {}
local block = {[vkeys.VK_RETURN] = true, [vkeys.VK_T] = true, [vkeys.VK_F6] = true, [vkeys.VK_F8] = true}

lua_thread.create(function ()
	while true do
		wait(0)
		for k, v in ipairs(list) do
			if module.isKeyPressed(v.keys) then
				v.callback(v.keys)
			end
		end
	end
end)

function module.getKeyName(keys)
	local result = {}
	for k, v in ipairs(keys) do
		table.insert(result, vkeys.id_to_name(v))
	end
	return table.concat(result, " + ")
end

function module.getKeyPressed()
	local keys = {}
	local state = false
	for k, v in ipairs({VK_LSHIFT, VK_RSHIFT, VK_LCONTROL, VK_RCONTROL, VK_LMENU, VK_RMENU}) do
		if isKeyDown(v) then table.insert(keys, v) end
	end
	for k, v in pairs(vkeys) do
		if isKeyDown(v) and (v ~= VK_MENU and v ~= VK_CONTROL and v ~= VK_SHIFT and v ~= VK_LMENU and v ~= VK_RMENU and v ~= VK_RCONTROL and v ~= VK_LCONTROL and v ~= VK_LSHIFT and v ~= VK_RSHIFT) and not state and not block[v] then
			table.insert(keys, v)
			state = true
		end
	end
	return state, keys
end

function module.isKeyPressed(keys)
	local count = 0
	for k, v in ipairs(keys) do
		if k == #keys and isKeyJustPressed(v) then count = count + 1
		elseif k ~= #keys and isKeyDown(v) then count = count + 1 end
	end
	return count == #keys and true or false
end

function module.isHotKeyDefined(keys)
	for k, v in ipairs(list) do if module.getKeyName(v.keys) == module.getKeyName(keys) then return true end end
	return false
end

function module.registerHotKey(keys, callback)
	if module.isHotKeyDefined(keys) then return false end
	table.insert(list, {keys = keys, callback = callback})
	return true
end

function module.unRegisterHotKey(keys)
	for k, v in ipairs(list) do
		if v.keys == keys then
			table.remove(list, k)
			return true
		end
	end
	return false
end

function module.HotKey(keys, size)
	local keys = keys or {}
	local bool, name = false
	local size = size or imgui.ImVec2(0, 0)
	if module.edit == keys then
		local state, result = module.getKeyPressed()
		if state then
			bool = true
			keys.l = keys
			keys.n = result
			module.edit = false
			name = module.getKeyName(result)
		elseif #result > 0 then name = module.getKeyName(result)
		else name = os.time() % 2 == 0 and "не указано" or "" end
	else
		local key = module.getKeyName(keys)
		name = key:len() > 0 and key or "не указано"
	end
	imgui.PushStyleColor(imgui.Col.Button, imgui.GetStyle().Colors[imgui.Col.FrameBg])
	imgui.PushStyleColor(imgui.Col.ButtonHovered, imgui.GetStyle().Colors[imgui.Col.FrameBgHovered])
	imgui.PushStyleColor(imgui.Col.ButtonActive, imgui.GetStyle().Colors[imgui.Col.FrameBgActive])
	if imgui.Button(name, size) and not module.edit then module.edit = keys end
	imgui.PopStyleColor(imgui.Col.WindowBg)
	return bool
end

return module