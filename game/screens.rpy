init offset = -1

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")

style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5

style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")

style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

################################################################################
## Диалоговое окно в стиле «Зайчика»
################################################################################

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        background Solid("#0b0b0dfa")
        xysize (1500, 230)
        xalign 0.5
        yalign 0.95
        padding (50, 30, 50, 30)

        if who:
            window:
                id "namebox"
                background Solid("#141418ff")
                padding (25, 8, 25, 8)
                pos (45, -42)

                text who id "who"

        fixed:
            xfill True
            yfill True

            text what id "what":
                xpos 0
                ypos 0
                xsize 1400
                ymaximum 105

            hbox:
                xalign 0.5
                yalign 1.0
                spacing 35

                textbutton _("<") action Rollback() text_color "#8c8c8c" text_hover_color "#ffffff"
                textbutton _(">") action NullAction() text_color "#444444"
                textbutton _("SKIP") action Skip() text_color "#8c8c8c" text_hover_color "#ffffff"
                textbutton _("LOG") action ShowMenu("history") text_color "#8c8c8c" text_hover_color "#ffffff"
                textbutton _("OPT") action ShowMenu("preferences") text_color "#8c8c8c" text_hover_color "#ffffff"

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

init python:
    config.character_id_prefixes.append("namebox")

style window is default
style say_label is default
style say_dialogue is default
style namebox is default
style namebox_label is say_label

style say_dialogue:
    xmaximum 1400
    color "#ffffff"
    size gui.text_size

style say_label:
    color "#ffffff"
    size gui.name_text_size

style namebox:
    xalign 0.0

################################################################################
## Базовые экраны меню (чтобы движок не ругался)
################################################################################

screen choice(items):
    style_prefix "choice"
    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing
        for i in items:
            textbutton i.caption action i.action

screen main_menu():
    tag menu
    add gui.main_menu_background
    use navigation

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):
    style_prefix "game_menu"
    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background
    frame:
        style "game_menu_outer_frame"
        transclude
    use navigation
    textbutton _("Return"):
        style "return_button"
        action Return()
    label title

screen navigation():
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing
        if main_menu:
            textbutton _("Start") action Start()
        else:
            textbutton _("History") action ShowMenu("history")
            textbutton _("Save") action ShowMenu("save")
        textbutton _("Load") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        if not main_menu:
            textbutton _("Main Menu") action MainMenu()
        textbutton _("Quit") action Quit(confirm=not main_menu)

screen about():
    tag menu
    use game_menu(_("About"))

screen save():
    tag menu
    use game_menu(_("Save"))

screen load():
    tag menu
    use game_menu(_("Load"))

screen preferences():
    tag menu
    use game_menu(_("Preferences"))

screen history():
    tag menu
    use game_menu(_("History"))

screen help():
    tag menu
    use game_menu(_("Help"))

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    frame:
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 45
            label _(message):
                style "confirm_prompt"
                xalign 0.5
            hbox:
                xalign 0.5
                spacing 150
                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

screen skip_indicator():
    zorder 100
    style_prefix "skip"
    frame:
        text _("Skipping")

screen notify(message):
    zorder 100
    style_prefix "notify"
    frame:
        text "[message!t]"
    timer 3.25 action Hide("notify")

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"
        text "NVL Mode"