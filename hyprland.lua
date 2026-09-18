local active_border_color = "rgb(1e1e1e)"
local inactive_border_color = "rgb(808080)"

hl.config({
	general = {
		border_size = 3,
		gaps_in = 6,
		gaps_out = 10,
		col = {
			active_border = active_border_color,
			inactive_border = inactive_border_color,
		},
	},

	decoration = {
		rounding = 0,
		active_opacity = 1,
		inactive_opacity = 1,
	},

	group = {
		col = {
			border_active = active_border_color,
			border_inactive = inactive_border_color,
		},
	},
})
