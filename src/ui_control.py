import os
import numpy as np
import time
import cv2
from functools import cache
from dataclasses import dataclass

from config import Config


@dataclass
class ScreenObject:
    _screen_object = None
    name: list[str]
    roi_name: str = None
    threshold: float = 0.68
    best_match: bool = False
    use_grayscale: bool = False
    color_match: list[np.array] = None

    def __call__(self, cls):
        cls._screen_object = self
        return cls


class ScreenObjects:
    InGame = ScreenObject(
        name=["GAMEBAR_ANCHOR", "GAMEBAR_ANCHOR_DARK"],
        roi_name="gamebar_anchor",
        threshold=0.8,
        best_match=True,
        use_grayscale=True
    )
    WaypointLabel = ScreenObject(
        name=["LABEL_WAYPOINT"],
        roi_name="left_panel_header",
        threshold=0.8,
        use_grayscale=True
    )
    WaypointTabs = ScreenObject(
        name=["WP_A1_ACTIVE", "WP_A2_ACTIVE", "WP_A3_ACTIVE", "WP_A4_ACTIVE", "WP_A5_ACTIVE"],
        roi_name="wp_act_roi_name",
        threshold=0.8,
        best_match=True,
        use_grayscale=True
    )
    MercIcon = ScreenObject(
        name=["MERC_A2", "MERC_A1", "MERC_A5", "MERC_A3"],
        roi_name="merc_icon",
        threshold=0.9,
        use_grayscale=True
    )
    PlayBtn = ScreenObject(
        name=["PLAY_BTN", "PLAY_BTN_GRAY"],
        roi_name="play_btn",
        best_match=True,
        use_grayscale=True
    )
    MainMenu = ScreenObject(
        name=["MAIN_MENU_TOP_LEFT", "MAIN_MENU_TOP_LEFT_DARK"],
        roi_name="main_menu_top_left",
        best_match=True,
        use_grayscale=True
    )
    Loading = ScreenObject(
        name=["LOADING", "CREATING_GAME"],
        roi_name="difficulty_select",
        threshold=0.9,
        use_grayscale=True
    )
    CubeInventory = ScreenObject(
        name=["HORADRIC_CUBE"],
        roi_name="left_inventory",
        threshold=0.8,
        use_grayscale=True
    )
    CubeOpened = ScreenObject(
        name=["CUBE_TRANSMUTE_BTN"],
        roi_name="cube_btn_roi_name",
        threshold=0.8,
        use_grayscale=True
    )
    OnlineStatus = ScreenObject(
        name=["CHARACTER_STATE_ONLINE", "CHARACTER_STATE_OFFLINE"],
        roi_name="character_online_status",
        best_match=True,
    )
    SelectedCharacter = ScreenObject(
        name=["CHARACTER_ACTIVE"],
        roi_name="character_select",
        threshold=0.8,
    )
    ServerError = ScreenObject(
        name=["SERVER_ISSUES"]
    )
    SaveAndExit = ScreenObject(
        name=["SAVE_AND_EXIT_NO_HIGHLIGHT", "SAVE_AND_EXIT_HIGHLIGHT"],
        roi_name="save_and_exit",
        threshold=0.85,
        use_grayscale=True
    )
    NeedRepair = ScreenObject(
        name=["REPAIR_NEEDED"],
        roi_name="repair_needed"
    )
    ItemPickupText = ScreenObject(
        name=["ITEM_PICKUP_ENABLED", "ITEM_PICKUP_DISABLED"],
        roi_name="chat_line_1",
        best_match=True
    )
    ShrineArea = ScreenObject(
        name=["SHRINE", "HIDDEN_STASH", "SKULL_PILE"],
        roi_name="shrine_check",
        threshold=0.8
    )
    TownPortal = ScreenObject(
        name=["BLUE_PORTAL"],
        threshold=0.8,
        roi_name="tp_search"
    )
    TownPortalReduced = ScreenObject(
        name=["BLUE_PORTAL"],
        threshold=0.8,
        roi_name="reduce_to_center"
    )
    GoldBtnInventory = ScreenObject(
        name=["INVENTORY_GOLD_BTN"],
        roi_name="gold_btn",
        use_grayscale=True
    )
    GoldBtnStash = ScreenObject(
        name=["INVENTORY_GOLD_BTN"],
        roi_name="gold_btn_stash"
    )
    GoldBtnVendor = ScreenObject(
        name=["VENDOR_GOLD"],
        roi_name="gold_btn_stash"
    )
    GoldNone = ScreenObject(
        name=["INVENTORY_NO_GOLD"],
        roi_name="inventory_gold",
        threshold=0.83
    )
    TownPortalSkill = ScreenObject(
        name=["TP_ACTIVE", "TP_INACTIVE"],
        roi_name="skill_right",
        best_match=True,
        threshold=0.79
    )
    RepairBtn = ScreenObject(
        name=["REPAIR_BTN"],
        roi_name="repair_btn",
        use_grayscale=True
    )
    YouHaveDied = ScreenObject(
        name=["YOU_HAVE_DIED"],
        roi_name="death",
        threshold=0.9,
        color_match=Config().colors["red"],
        use_grayscale=True
    )
    Overburdened = ScreenObject(
        name=["INVENTORY_FULL_MSG_0", "INVENTORY_FULL_MSG_1"],
        roi_name="chat_line_1",
        threshold=0.9
    )
    Corpse = ScreenObject(
        name=["CORPSE", "CORPSE_2", "CORPSE_BARB", "CORPSE_DRU", "CORPSE_NEC", "CORPSE_PAL", "CORPSE_SIN",
              "CORPSE_SORC",
              "CORPSE_ZON"],
        roi_name="corpse",
        threshold=0.8
    )
    BeltExpandable = ScreenObject(
        name=["BELT_EXPANDABLE"],
        roi_name="gamebar_belt_expandable",
        threshold=0.8
    )
    NPCMenu = ScreenObject(
        name=["TALK", "CANCEL"],
        threshold=0.8,
        use_grayscale=True
    )
    ChatIcon = ScreenObject(
        name=["CHAT_ICON"],
        roi_name="chat_icon",
        threshold=0.8,
        use_grayscale=True
    )
    LeftPanel = ScreenObject(
        name=["CLOSE_PANEL"],
        roi_name="left_panel_header",
        threshold=0.8,
        use_grayscale=True
    )
    RightPanel = ScreenObject(
        name=["CLOSE_PANEL", "CLOSE_PANEL_2"],
        roi_name="right_panel_header",
        threshold=0.8,
        use_grayscale=True
    )
    NPCDialogue = ScreenObject(
        name=["NPC_DIALOGUE"],
        roi_name="npc_dialogue",
        threshold=0.8,
        use_grayscale=True
    )
    SkillsExpanded = ScreenObject(
        name=["BIND_SKILL"],
        roi_name="bind_skill",
        threshold=0.8,
        use_grayscale=True
    )
    Unidentified = ScreenObject(
        name=["UNIDENTIFIED"],
        threshold=0.8,
        color_match=Config().colors["red"]
    )
    Key = ScreenObject(
        name=["INV_KEY"],
        threshold=0.8
    )
    EmptyStashSlot = ScreenObject(
        name=["STASH_EMPTY_SLOT"],
        roi_name="left_inventory",
        threshold=0.8,
    )
    NotEnoughGold = ScreenObject(
        name=["NOT_ENOUGH_GOLD"],
        threshold=0.9,
        color_match=Config().colors["red"],
        use_grayscale=True
    )
    QuestSkillBtn = ScreenObject(
        name=["QUEST_SKILL_BTN"],
        threshold=0.9,
        use_grayscale=True,
        roi_name="quest_skill_btn"
    )
    TabIndicator = ScreenObject(
        name=["TAB_INDICATOR"],
        roi_name="tab_indicator",
    )
    DepositBtn = ScreenObject(
        name=["DEPOSIT_BTN", "DEPOSIT_BTN_BRIGHT"],
        threshold=0.8,
        roi_name="deposit_btn",
    )
    InventoryBackground = ScreenObject(
        name=["INVENTORY_BG_PATTERN"],
        roi_name="inventory_bg_pattern",
        threshold=0.8,
    )
