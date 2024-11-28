local imgui = require 'imgui'
imgui.ShowCursor = false
local style = imgui.GetStyle()
local colors = style.Colors
local clr = imgui.Col
local ImVec4 = imgui.ImVec4
local encoding = require 'encoding'
u8 = encoding.UTF8
encoding.default = 'CP1251'
imgui.GetStyle().WindowMinSize = imgui.ImVec2(1.0, 1.0)
local ToScreen = convertGameScreenCoordsToWindowScreenCoords
local sX, sY = ToScreen(630, 438)
local message = {}
local typeStyle = {
	{ -- 1 - normal message
		text = imgui.ImColor(255, 255, 255, 255):GetVec4(),
		rightBox = imgui.ImColor(0, 0, 0, 255):GetU32(),
		mainBox = {
			imgui.ImColor(0, 0, 0, 170):GetU32(), -- left top
			imgui.ImColor(0, 0, 0, 235):GetU32(), -- right top
			imgui.ImColor(0, 0, 0, 235):GetU32(), -- left button
			imgui.ImColor(0, 0, 0, 170):GetU32(), -- right button
		}
	},
	{ -- 2 - info message
		text = imgui.ImColor(255, 255, 255, 255):GetVec4(),
		rightBox = imgui.ImColor(0, 157, 194, 255):GetU32(),
		mainBox = {
			imgui.ImColor(0, 137, 174, 170):GetU32(), -- left top
			imgui.ImColor(0, 137, 174, 235):GetU32(), -- right top
			imgui.ImColor(0, 137, 174, 235):GetU32(), -- left button
			imgui.ImColor(0, 137, 174, 170):GetU32(), -- right button
		}
	},
	{ -- 3 - error message
		text = imgui.ImColor(255, 255, 255, 255):GetVec4(),
		rightBox = imgui.ImColor(190, 40, 40, 255):GetU32(),
		mainBox = {
			imgui.ImColor(170, 20, 20, 170):GetU32(), -- left top
			imgui.ImColor(170, 20, 20, 235):GetU32(), -- right top
			imgui.ImColor(170, 20, 20, 235):GetU32(), -- left button
			imgui.ImColor(170, 20, 20, 170):GetU32(), -- right button
		}
	}
}
local msxMsg = 3
local notfList = {
	pos = {
		x = sX - 200,
		y = sY
	},
	npos = {
		x = sX - 200,
		y = sY
	},
	size = {
		x = 200,
		y = 0
	}
}

local LastActiveTime = {}
local LastActive = {}
local LastStatus = {}

function setstyle()
	style.WindowRounding = 2.0
	style.WindowTitleAlign = imgui.ImVec2(0.5, 0.5)
	style.ChildWindowRounding = 2.0
	style.FrameRounding = 2.0
	style.ItemSpacing = imgui.ImVec2(5.0, 4.0)
	style.ScrollbarSize = 13.0
	style.ScrollbarRounding = 0
	style.GrabMinSize = 8.0
	style.GrabRounding = 1.0
	-- style.Alpha =
	style.WindowPadding = imgui.ImVec2(4.0, 4.0)
	style.WindowMinSize = imgui.ImVec2(1.0, 1.0)
	style.FramePadding = imgui.ImVec2(3.5, 3.5)
	-- style.ItemInnerSpacing =
	-- style.TouchExtraPadding =
	-- style.IndentSpacing =
	-- style.ColumnsMinSpacing = ?
	style.ButtonTextAlign = imgui.ImVec2(0.0, 0.5)
	-- style.DisplayWindowPadding =
	-- style.DisplaySafeAreaPadding =
	-- style.AntiAliasedLines =
	-- style.AntiAliasedShapes =
	-- style.CurveTessellationTol =

	colors[clr.Text]                   = ImVec4(1.00, 1.00, 1.00, 1.00)
	colors[clr.TextDisabled]           = ImVec4(0.50, 0.50, 0.50, 1.00)
	colors[clr.WindowBg]               = ImVec4(0.06, 0.06, 0.06, 0.00)
	colors[clr.ChildWindowBg]          = ImVec4(1.00, 1.00, 1.00, 0.00)
	colors[clr.PopupBg]                = ImVec4(0.08, 0.08, 0.08, 0.94)
	colors[clr.ComboBg]                = colors[clr.PopupBg]
	colors[clr.Border]                 = ImVec4(0.43, 0.43, 0.50, 0.50)
	colors[clr.BorderShadow]           = ImVec4(0.00, 0.00, 0.00, 0.00)
	colors[clr.FrameBg]                = ImVec4(0.12, 0.12, 0.12, 0.94)
	colors[clr.FrameBgHovered]         = ImVec4(0.45, 0.45, 0.45, 0.85)
	colors[clr.FrameBgActive]          = ImVec4(0.63, 0.63, 0.63, 0.63)
	colors[clr.TitleBg]                = ImVec4(0.13, 0.13, 0.13, 0.99)
	colors[clr.TitleBgActive]          = ImVec4(0.13, 0.13, 0.13, 0.99)
	colors[clr.TitleBgCollapsed]       = ImVec4(0.05, 0.05, 0.05, 0.79)
	colors[clr.MenuBarBg]              = ImVec4(0.14, 0.14, 0.14, 1.00)
	colors[clr.ScrollbarBg]            = ImVec4(0.02, 0.02, 0.02, 0.53)
	colors[clr.ScrollbarGrab]          = ImVec4(0.31, 0.31, 0.31, 1.00)
	colors[clr.ScrollbarGrabHovered]   = ImVec4(0.41, 0.41, 0.41, 1.00)
	colors[clr.ScrollbarGrabActive]    = ImVec4(0.51, 0.51, 0.51, 1.00)
	colors[clr.CheckMark]              = ImVec4(1.00, 1.00, 1.00, 1.00)
	colors[clr.SliderGrab]             = ImVec4(0.28, 0.28, 0.28, 1.00)
	colors[clr.SliderGrabActive]       = ImVec4(0.35, 0.35, 0.35, 1.00)
	colors[clr.Button]                 = ImVec4(0.12, 0.12, 0.12, 0.94)
	colors[clr.ButtonHovered]          = ImVec4(0.34, 0.34, 0.35, 0.89)
	colors[clr.ButtonActive]           = ImVec4(0.21, 0.21, 0.21, 0.81)
	colors[clr.Header]                 = ImVec4(0.12, 0.12, 0.12, 0.94)
	colors[clr.HeaderHovered]          = ImVec4(0.34, 0.34, 0.35, 0.89)
	colors[clr.HeaderActive]           = ImVec4(0.12, 0.12, 0.12, 0.94)
	colors[clr.Separator]              = colors[clr.Border]
	colors[clr.SeparatorHovered]       = ImVec4(0.26, 0.59, 0.98, 0.78)
	colors[clr.SeparatorActive]        = ImVec4(0.26, 0.59, 0.98, 1.00)
	colors[clr.ResizeGrip]             = ImVec4(0.26, 0.59, 0.98, 0.25)
	colors[clr.ResizeGripHovered]      = ImVec4(0.26, 0.59, 0.98, 0.67)
	colors[clr.ResizeGripActive]       = ImVec4(0.26, 0.59, 0.98, 0.95)
	colors[clr.CloseButton]            = ImVec4(0.41, 0.41, 0.41, 0.50)
	colors[clr.CloseButtonHovered]     = ImVec4(0.98, 0.39, 0.36, 1.00)
	colors[clr.CloseButtonActive]      = ImVec4(0.98, 0.39, 0.36, 1.00)
	colors[clr.PlotLines]              = ImVec4(0.61, 0.61, 0.61, 1.00)
	colors[clr.PlotLinesHovered]       = ImVec4(1.00, 0.43, 0.35, 1.00)
	colors[clr.PlotHistogram]          = ImVec4(0.90, 0.70, 0.00, 1.00)
	colors[clr.PlotHistogramHovered]   = ImVec4(1.00, 0.60, 0.00, 1.00)
	colors[clr.TextSelectedBg]         = ImVec4(0.26, 0.59, 0.98, 0.35)
	colors[clr.ModalWindowDarkening]   = ImVec4(0.80, 0.80, 0.80, 0.35)
end

function main()
	while true do
		wait(0)
		imgui.ShowCursor = false
		imgui.Process = #message > 0
	end
end

function ImSaturate(f)
	return f < 0.0 and 0.0 or (f > 1.0 and 1.0 or f)
 end

local glyph_ranges = nil
function imgui.BeforeDrawFrame()
	local x, y = getScreenResolution()
    if not fontChanged then
		setstyle()
        fontChanged = true
        glyph_ranges = imgui.GetIO().Fonts:GetGlyphRangesCyrillic()
        imgui.GetIO().Fonts:Clear()
        imgui.GetIO().Fonts:AddFontFromFileTTF(getFolderPath(0x14) .. '\\arialbd.ttf', y < 1080 and 14 or 15, nil, glyph_ranges)
		imgui.RebuildFonts()
    end
end

function imgui.OnDrawFrame()
	imgui.SetMouseCursor(imgui.MouseCursor.None)
	onRenderNotification()
end

function onRenderNotification()
    local ANIM_SPEED = 0.3
	local count = 0
	for k, v in ipairs(message) do
		local push = false
		if v.active and v.time < os.clock() then
			v.active = false
		end
		if count < 5 then
			if not v.active then
				if v.showtime > 0 then
					v.active = true
					v.time = os.clock() + v.showtime
					v.showtime = 0
					LastActiveTime[k] = os.clock()
					LastActive[k] = true
					LastStatus[k] = true
				end
			end
			if v.active then
				count = count + 1
				local t = LastStatus[k] and 0.0 or 1.0
				if LastActive[k] then
					local time = os.clock() - LastActiveTime[k]
					if time <= ANIM_SPEED then
						local t_anim = ImSaturate(time / ANIM_SPEED)
						t = LastStatus[k] and 1.0 - t_anim or t_anim
					else
						LastActive[k] = false
					end
				end
				if v.time - os.clock() <= ANIM_SPEED and not LastActive[k] and LastStatus[k] then
					LastStatus[k] = false
					LastActiveTime[k] = os.clock()
					LastActive[k] = true
				end
				local nText = u8(tostring(v.text))
				notfList.size = imgui.GetFont():CalcTextSizeA(imgui.GetFont().FontSize, 200.0, 196.0, nText)
				notfList.pos = imgui.ImVec2(notfList.pos.x + t * 215, notfList.pos.y - (notfList.size.y + (count == 1 and 8 or 13)))
				imgui.SetNextWindowPos(notfList.pos, _, imgui.ImVec2(0.0, 0.0))
				imgui.SetNextWindowSize(imgui.ImVec2(215 - t * 215, notfList.size.y + imgui.GetStyle().ItemSpacing.y + imgui.GetStyle().WindowPadding.y))

				imgui.Begin(u8'##msg' .. k, _, imgui.WindowFlags.NoCollapse + imgui.WindowFlags.NoResize + imgui.WindowFlags.NoScrollbar + imgui.WindowFlags.NoMove + imgui.WindowFlags.NoTitleBar)

				local style
				if type(v.style) == "table" then
					style = v.style
				else
					style = typeStyle[v.style] or typeStyle[1]
				end

				local draw_list = imgui.GetWindowDrawList()
				local p = imgui.GetCursorScreenPos()
				draw_list:AddRectFilledMultiColor(imgui.ImVec2(p.x - imgui.GetStyle().WindowPadding.x - 20, p.y - imgui.GetStyle().WindowPadding.y), imgui.ImVec2(p.x + 200, p.y + notfList.size.y + imgui.GetStyle().ItemSpacing.y + imgui.GetStyle().WindowPadding.y), style.mainBox[1], style.mainBox[2], style.mainBox[3], style.mainBox[4]);
				draw_list:AddRectFilled(imgui.ImVec2(p.x - imgui.GetStyle().WindowPadding.x + 205, p.y - imgui.GetStyle().WindowPadding.y), imgui.ImVec2(p.x + 216, p.y + notfList.size.y + imgui.GetStyle().ItemSpacing.y + imgui.GetStyle().WindowPadding.y), style.rightBox);

				imgui.PushTextWrapPos(196.0)
				imgui.TextColored(style.text, nText)
				imgui.PopTextWrapPos()

				imgui.End()
			end
		end
	end
	sX, sY = ToScreen(630, 438)
	notfList = {
		pos = {
			x = sX - 200,
			y = sY
		},
		npos = {
			x = sX - 200,
			y = sY
		},
		size = {
			x = 200,
			y = 0
		}
	}
end

function EXPORTS.addNotification(text, time, style)
	local style = style or 1
	message[#message+1] = {active = false, time = 0, showtime = time, text = text, style = style}
end
