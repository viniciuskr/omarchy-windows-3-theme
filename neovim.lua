-- Windows 3 — self-contained Neovim colorscheme
-- TypeSafe AI / Windows 3.1 VGA navy. Works without extra plugins.

local colors = {
	bg = "#fefefe",
	fg = "#1e1e1e",
	muted = "#858585",
	dark = "#e8e8f0",
	border = "#1e1e1e",
	selection = "#000080",
	navy = "#000080",
	blue = "#0000ff",
	teal = "#09aea1",
	green = "#03aa5c",
	red = "#800000",
	yellow = "#c9a227",
	magenta = "#800080",
	silver = "#c0c0c0",
	sage = "#abbab9",
	white = "#fefefe",
}

local function set_hl(group, opts)
	vim.api.nvim_set_hl(0, group, opts)
end

return {
	{
		"LazyVim/LazyVim",
		opts = {
			colorscheme = function()
				vim.cmd("set termguicolors")
				vim.cmd("highlight clear")
				if vim.fn.exists("syntax_on") == 1 then
					vim.cmd("syntax reset")
				end

				set_hl("Normal", { fg = colors.fg, bg = colors.bg })
				set_hl("NormalNC", { fg = colors.fg, bg = colors.bg })
				set_hl("NormalFloat", { fg = colors.fg, bg = colors.silver })
				set_hl("FloatBorder", { fg = colors.border, bg = colors.silver })
				set_hl("Comment", { fg = colors.muted, italic = true })
				set_hl("NonText", { fg = colors.muted })
				set_hl("Whitespace", { fg = colors.muted })
				set_hl("EndOfBuffer", { fg = colors.bg })

				set_hl("Cursor", { fg = colors.bg, bg = colors.fg })
				set_hl("CursorLine", { bg = colors.dark })
				set_hl("CursorColumn", { bg = colors.dark })
				set_hl("CursorLineNr", { fg = colors.navy, bold = true })
				set_hl("LineNr", { fg = colors.muted })
				set_hl("SignColumn", { bg = colors.bg })
				set_hl("ColorColumn", { bg = colors.dark })

				set_hl("Visual", { fg = colors.white, bg = colors.selection })
				set_hl("Search", { fg = colors.white, bg = colors.navy })
				set_hl("IncSearch", { fg = colors.white, bg = colors.teal })
				set_hl("MatchParen", { fg = colors.teal, bold = true })

				set_hl("VertSplit", { fg = colors.border })
				set_hl("WinSeparator", { fg = colors.border })

				set_hl("StatusLine", { fg = colors.white, bg = colors.navy, bold = true })
				set_hl("StatusLineNC", { fg = colors.fg, bg = colors.silver })
				set_hl("WinBar", { fg = colors.white, bg = colors.navy })
				set_hl("WinBarNC", { fg = colors.silver, bg = colors.navy })

				set_hl("TabLine", { fg = colors.fg, bg = colors.silver })
				set_hl("TabLineFill", { bg = colors.navy })
				set_hl("TabLineSel", { fg = colors.white, bg = colors.navy, bold = true })

				set_hl("Pmenu", { fg = colors.fg, bg = colors.silver })
				set_hl("PmenuSel", { fg = colors.white, bg = colors.navy })
				set_hl("PmenuSbar", { bg = colors.sage })
				set_hl("PmenuThumb", { bg = colors.navy })

				set_hl("Constant", { fg = colors.magenta })
				set_hl("String", { fg = colors.green })
				set_hl("Character", { fg = colors.green })
				set_hl("Number", { fg = colors.magenta })
				set_hl("Boolean", { fg = colors.navy, bold = true })
				set_hl("Float", { fg = colors.magenta })

				set_hl("Identifier", { fg = colors.fg })
				set_hl("Function", { fg = colors.navy, bold = true })

				set_hl("Statement", { fg = colors.navy, bold = true })
				set_hl("Conditional", { fg = colors.navy })
				set_hl("Repeat", { fg = colors.navy })
				set_hl("Keyword", { fg = colors.navy, bold = true })
				set_hl("Operator", { fg = colors.teal })
				set_hl("Exception", { fg = colors.red })

				set_hl("Type", { fg = colors.teal, italic = true })
				set_hl("StorageClass", { fg = colors.red })
				set_hl("Structure", { fg = colors.green })
				set_hl("Typedef", { fg = colors.green })

				set_hl("PreProc", { fg = colors.blue })
				set_hl("Include", { fg = colors.navy })
				set_hl("Define", { fg = colors.navy })
				set_hl("Macro", { fg = colors.yellow })

				set_hl("Special", { fg = colors.teal })
				set_hl("Delimiter", { fg = colors.fg })
				set_hl("Title", { fg = colors.navy, bold = true })
				set_hl("Todo", { fg = colors.bg, bg = colors.yellow, bold = true })

				set_hl("DiffAdd", { fg = colors.green, bg = colors.dark })
				set_hl("DiffChange", { fg = colors.yellow, bg = colors.dark })
				set_hl("DiffDelete", { fg = colors.red, bg = colors.dark })
				set_hl("DiffText", { fg = colors.white, bg = colors.navy })

				set_hl("DiagnosticError", { fg = colors.red })
				set_hl("DiagnosticWarn", { fg = colors.yellow })
				set_hl("DiagnosticInfo", { fg = colors.teal })
				set_hl("DiagnosticHint", { fg = colors.muted })
				set_hl("DiagnosticUnderlineError", { undercurl = true, sp = colors.red })
				set_hl("DiagnosticUnderlineWarn", { undercurl = true, sp = colors.yellow })
				set_hl("DiagnosticUnderlineInfo", { undercurl = true, sp = colors.teal })
				set_hl("DiagnosticUnderlineHint", { undercurl = true, sp = colors.muted })

				set_hl("@comment", { link = "Comment" })
				set_hl("@string", { link = "String" })
				set_hl("@number", { link = "Number" })
				set_hl("@boolean", { link = "Boolean" })
				set_hl("@constant", { link = "Constant" })
				set_hl("@function", { link = "Function" })
				set_hl("@function.builtin", { fg = colors.teal, bold = true })
				set_hl("@keyword", { link = "Keyword" })
				set_hl("@type", { link = "Type" })
				set_hl("@variable", { fg = colors.fg })
				set_hl("@variable.builtin", { fg = colors.red, italic = true })
				set_hl("@property", { fg = colors.navy })
				set_hl("@operator", { link = "Operator" })
				set_hl("@punctuation.delimiter", { link = "Delimiter" })
				set_hl("@punctuation.bracket", { link = "Delimiter" })

				vim.g.colors_name = "windows-3"
			end,
		},
	},
}
