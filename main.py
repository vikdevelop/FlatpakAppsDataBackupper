import gi
import os
import glob
import shutil
from datetime import date
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
HOME = os.path.expanduser('~')
date = date.today()

class Dialog_export(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Package list has been created!", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label()
        label.set_markup("<b>Done!</b> Data of Flatpak apps has been exported successfully! File is in: <i>%s/Flatpak_Apps_Data/Flatpak_Apps_Data_%s.tar.gz</i>" % (HOME, date))

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Dialog_import(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Import data of Flatpak applications", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label()
        label.set_markup("<b>Done!</b>Data has been imported on your OS successfully! Data has been imported successfully to: <i>%s/.var/app/</i>" % HOME)

        box2 = self.get_content_area()
        box.add(label)
        self.show_all()

class PKGBackerWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, title="Flatpak applications data backupper")
        self.set_default_size(600, 200)

        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(mainBox)

        self.label = Gtk.Label()
        mainBox.pack_start(self.label, True, True, 0)

        self.label_h1 = Gtk.Label()
        self.label_h1.set_markup("<b>Export Flatpak Apps Data</b>")
        mainBox.pack_start(self.label_h1, True, True, 0)

        self.button_export = Gtk.Button(label="Export")
        self.button_export.connect("clicked", self.on_button_export)
        mainBox.pack_start(self.button_export, True, True, 0)

        self.label_h2 = Gtk.Label()
        self.label_h2.set_markup("<b>Import Flatpak Apps Data</b>")
        mainBox.pack_start(self.label_h2, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter directory to archive with imported flatpak apps data (eg. /home/user/Flatpak)")
        mainBox.pack_start(self.entry, True, True, 0)

        self.button_importb = Gtk.Button(label="Import")
        self.button_importb.connect("clicked", self.on_button_importb)
        mainBox.pack_start(self.button_importb, True, True, 0)

    def on_button_export(self, widget, *args):
        """ button "clicked" in event buttonStart. """
        self.export()

    def on_button_importb(self, widget, *args):
        self.importb()

    def on_SpinnerWindow_destroy(self, widget, *args):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        Gtk.main_quit()

    def export(self):
        print("cd $HOME/.var")
        os.chdir("%s/.var" % HOME)
        print("Compressing archive...")
        if not os.path.exists("%s/Flatpak_Apps_Data" % HOME):
            os.mkdir("%s/Flatpak_Apps_Data" % HOME)
        os.system("tar --gz -cf Flatpak_Apps_Data_%s.tar.gz ./" % date)
        shutil.move("Flatpak_Apps_Data_%s.tar.gz" % date, "%s/Flatpak_Apps_Data/" % HOME)
        # Dialog_create window
        dialog_e = Dialog_export(self)
        response_e = dialog_e.run()

        if response_e == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response_e == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog_e.destroy()

    def importb(self):
        entry = self.entry.get_text()
        os.chdir("%s" % entry)
        if not os.path.exists("%s/.var/app" % HOME):
            os.makedirs("%s/.var/app" % HOME)
        os.system("tar -xf *.tar.gz")
        shutil.move("app", "%s/.var/app" % HOME)
        # Dialog_import window
        dialog_m = Dialog_import(self)
        response_m = dialog_m.run()

        if response_m == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response_m == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog_m.destroy()

win = PKGBackerWindow()
win.show_all()
win.connect("delete-event", Gtk.main_quit)
Gtk.main()
