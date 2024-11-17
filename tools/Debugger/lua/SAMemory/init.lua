--[[
	Project: SA Memory (Available from https://blast.hk/)
	Developers: LUCHARE, FYP

	Special thanks:
		plugin-sdk (https://github.com/DK22Pac/plugin-sdk) for the structures and addresses.

	Copyright (c) 2018 BlastHack.
]]

local shared = require 'SAMemory.shared'

local ffi = shared.ffi
local cast = ffi.cast

local function PBOOL(x)
	return cast('bool *', x)
end

local function PVOID(x)
	return cast('void *', x)
end

local function PPVOID(x)
	return cast('void **', x)
end

return {
	_ver 								= '1.0.4';

	cast 								= cast;
	require 						= shared.require;

	code_pause					= PBOOL(0x00B7CB48);
	user_pause 					= PBOOL(0x00B7CB49);

	nullptr 						= PVOID(0x00000000);
	-- player camera (CCamera)
	camera 							= PVOID(0x00B6F028);
	-- weapon crosshairs (CWeaponEffects)
	crosshairs 					= PVOID(0x00C8A838); -- array[2]

	-- player ped (CPed)
	player_ped 				  = PPVOID(0x00B6F5F0);
	-- player vehicle (CVehicle)
	player_vehicle  		= PPVOID(0x00BA18FC);

	-- pools (CPool)
	ptrNodeSinglePool   = PPVOID(0x00B74484);
	ptrNodeDoublePool   = PPVOID(0x00B74488);
	ped_pool 						= PPVOID(0x00B74490);
	vehicle_pool 				= PPVOID(0x00B74494);
	building_pool 			= PPVOID(0x00B74498);
	object_pool 				= PPVOID(0x00B7449C);
	dummy_pool 					= PPVOID(0x00B744A0);
	colModelPool 			 	= PPVOID(0x00B744A4);
	task_pool 					= PPVOID(0x00B744A8);
	pedIntelligencePool = PPVOID(0x00B744C0);
}
