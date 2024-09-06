import logging

#
# Tk/Tcl module, only used for observable variables here.
# https://www.pythontutorial.net/tkinter/tkinter-stringvar/
from tkinter import IntVar, StringVar

import customtkinter

from src.app import App
from src.update_manager import UpdateManager
from src.gui import frames
from src.controllers import Keybinder
from src.gui.pages import (
    PageSelectCamera, PageKeyboard, PageAbout)

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("assets/themes/google_theme.json")

logger = logging.getLogger("MainGUi")

class MainGui:

    def __init__(self, tk_root):
        logger.info("Init MainGui")
        super().__init__()
        self.tk_root = tk_root

        # Get screen width and height for dynamic scaling
        screen_width = self.tk_root.winfo_screenwidth()
        screen_height = self.tk_root.winfo_screenheight()

        # Set window size based on screen dimensions for tablets
        if screen_width <= 1280:
            self.tk_root.geometry(f"{int(screen_width * 0.9)}x{int(screen_height * 0.9)}")
        else:
            self.tk_root.geometry("1024x800")

        self.tk_root.title(" ".join((App().name, App().version)))
        self.tk_root.iconbitmap("assets/images/icon.ico")
        self.tk_root.resizable(width=True, height=True)

        # Adjust scaling for higher-DPI displays
        self.tk_root.tk.call('tk', 'scaling', screen_width / 1280)

        # Configure rows and columns for grid responsiveness
        self.tk_root.grid_rowconfigure(1, weight=1)
        self.tk_root.grid_columnconfigure(1, weight=1)

        # Initialize observable variables
        self._updateState = None
        self.runningPublished = StringVar(self.tk_root, "")
        self.releasesSummary = StringVar(self.tk_root, "Update availability unknown.")
        self.installerSummary = StringVar(self.tk_root, "")
        self.installerPrompt = StringVar(self.tk_root, "")
        self.retrievingSize = IntVar(self.tk_root, 0)
        self.retrievedAmount = IntVar(self.tk_root, 0)

        # Create menu frame and assign callbacks
        self.frame_menu = frames.FrameMenu(self.tk_root,
                                           self.root_function_callback,
                                           height=360,
                                           width=260,
                                           logger_name="frame_menu")
        self.frame_menu.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=1, rowspan=3)

        # Create Preview frame
        self.frame_preview = frames.FrameCamPreview(self.tk_root,
                                                    self.cam_preview_callback,
                                                    logger_name="frame_preview")
        self.frame_preview.grid(row=1, column=0, padx=0, pady=0, sticky="sew", columnspan=1)
        self.frame_preview.enter()

        # Create all wizard pages and grid them
        self.pages = [
            PageSelectCamera(master=self.tk_root,),
            PageKeyboard(master=self.tk_root,),
            PageAbout(tkRoot=self.tk_root, updateHost=self)
        ]

        self.current_page_name = None
        for page in self.pages:
            page.grid(row=0, column=1, padx=5, pady=5, sticky="nsew", rowspan=2, columnspan=1)

        self.change_page(PageSelectCamera.__name__)

        # Profile UI
        self.frame_profile_switcher = frames.FrameProfileSwitcher(self.tk_root, main_gui_callback=self.root_function_callback)
        self.frame_profile_editor = frames.FrameProfileEditor(self.tk_root, main_gui_callback=self.root_function_callback)

        # Make layout adjustments for responsiveness
        self.adjust_layout_for_responsiveness()

    def adjust_layout_for_responsiveness(self):
        """Adjust layout dynamically based on screen size."""
        self.tk_root.update_idletasks()

        screen_width = self.tk_root.winfo_screenwidth()

        # Adjust frame widths dynamically based on screen width
        if screen_width <= 1280:  # Adjust for tablet-sized screens
            self.frame_menu.configure(width=200)  # Use configure instead of config
            self.frame_preview.configure(width=400)
        else:
            self.frame_menu.configure(width=260)
            self.frame_preview.configure(width=600)

        # Update layout again
        self.tk_root.update_idletasks()

    def root_function_callback(self, function_name, args: dict = {}, **kwargs):
        logger.info(f"root_function_callback {function_name} with {args}")

        # Basic page navigate
        if function_name == "change_page":
            self.change_page(args["target"])
            self.frame_menu.set_tab_active(tab_name=args["target"])

        # Profiles
        elif function_name == "show_profile_switcher":
            self.frame_profile_switcher.enter()
        elif function_name == "show_profile_editor":
            self.frame_profile_editor.enter()

        elif function_name == "refresh_profiles":
            logger.info("refresh_profile")
            for page in self.pages:
                page.refresh_profile()

    def cam_preview_callback(self, function_name, args: dict, **kwargs):
        logger.info(f"cam_preview_callback {function_name} with {args}")

        if function_name == "toggle_switch":
            self.set_mediapipe_mouse_enable(new_state=args["switch_status"])

    def set_mediapipe_mouse_enable(self, new_state: bool):
        if new_state:
            Keybinder().set_active(True)
        else:
            Keybinder().set_active(False)

    def change_page(self, target_page_name: str):

        if self.current_page_name == target_page_name:
            return

        for page in self.pages:
            if page.__class__.__name__ == target_page_name:
                page.grid()
                page.enter()
                self.current_page_name = page.__class__.__name__

            else:
                page.grid_remove()
                page.leave()

    def poll_update_state(self):
        updateState = UpdateManager().state
        if self._updateState is None or updateState != self._updateState:
            logger.info(f"updateState {updateState}.")
            # It looks like the trace() callback gets invoked after every set
            # call, even if the value didn't change.
            if self.releasesSummary.get() != updateState.releasesSummary:
                self.releasesSummary.set(updateState.releasesSummary)
            if self.installerSummary.get() != updateState.installerSummary:
                self.installerSummary.set(updateState.installerSummary)
            if self.installerPrompt.get() != updateState.installerPrompt:
                self.installerPrompt.set(updateState.installerPrompt)
            if self.runningPublished.get() != updateState.runningPublished:
                self.runningPublished.set(updateState.runningPublished)
        self._updateState = updateState

    def del_main_gui(self):
        logger.info("Deleting MainGui instance")
        # try:
        self.frame_preview.leave()
        self.frame_preview.destroy()
        self.frame_menu.leave()
        self.frame_menu.destroy()
        for page in self.pages:
            page.leave()
            page.destroy()

        self.tk_root.quit()
        self.tk_root.destroy()
