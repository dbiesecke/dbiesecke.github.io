import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'SuperN Wizard'
EXCLUDES       = [ADDON_ID, 'repository.Kodinoobs']
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 30
# Text File with build info in it.
BUILDFILE      = 'http://notjust4nerds.de/Kodi/Wizard/builds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE        = 'http://'
# Text File with retro info in it.  Leave as 'http://' to ignore
RETROFILE      = 'http://'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'YOUTUBE'
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'
# Text file for roms and emus
ROMPACK        = 'http://'
EMUAPKS        = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONMAINT      = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONAPK        = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONRETRO      = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONADDONS     = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONYOUTUBE    = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONSAVE       = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONTRAKT      = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONREAL       = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONLOGIN      = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONCONTACT    = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
ICONSETTINGS   = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'white'
COLOR2         = 'lawngreen'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']SuperN[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'Yes'
# You can add \n to do line breaks
CONTACT        = 'Danke schoen fuers installieren von Kodinoobs Wizard.\n\nKontakt findest du hier im auf der Webseite http://repo.kodinoobs.de'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
CONTACTFANART  = 'http://notjust4nerds.de/Kodi/Wizard/wizard_supern.png'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = 'http://repo.kodinoobs.de/plugin.program.kodinoobs.de.zip'
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = 'repository.Kodinoobs'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'http://ghostrepo.de/Plugins/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'http://repo.kodinoobs.de/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'No'
# Url to notification file
NOTIFICATION   = 'http://repo.kodinoobs.de/ApK/txt/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font14'
HEADERMESSAGE  = 'SuperN Wizard'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Font for Notification Window
FONTSETTINGS   = 'Font13'
# Background for Notification Window
BACKGROUND     = ''
#########################################################