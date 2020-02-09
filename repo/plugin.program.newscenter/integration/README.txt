###########################################################################
#
#          FILE:  plugin.program.newscenter
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.0.1
#       CREATED:  14.02.2016
#
###########################################################################
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.
#
###########################################################################
#     CHANGELOG:  (14.02.2016) TDOe - First Publishing
###########################################################################


Beschreibung:
=============

Das Plugin plugin.program.newscenter gibt Skinnern die Möglichkeit einen Nachrichten-Feed als Widget in den Skin zu integrieren.
Zudem können folgende Direktlinks per Pluginaufruf erfolgen:
- Tagesschau
- Tagesschau in 100s
- Kinder Nachrichten (logo)
- Wettervideos


Das Widget kann in den Settings konfiguriert werden, welcher Feed angezeigt werden soll. Hierzu stehen folgende NachrichtenQuellen zur Verfügung:
- Spiegel Online
- n-tv
- tagesschau.de
- n24
- Heise
- Google News
- FOCUS-Online
- Die Welt
- Sport 1
- ...

Desweiteren verfügt das Plugin über ein JSON File, in welchem Aenderungen an den Feeds als auch Neue Feeds hinzugefügt werden können. 
(NewsFeeds.json)

Im Bereich Sport stellt das NewsCenter Plugin die aktuelle Tabelle der 1. und 2. Bundesliga dar.

Ein weiteres JSON File (Buli.json) dient der Zuordnung der Ligaid zu Mannschaft (Benötigt für Vereinslogo)




Skintegration:
==============

Um das News-Widget in Confluence zu aktivieren, sind mehrere Schritte notwendig.



1. Dateien kopieren:
 
Die Datei "script-news.xml in den Confluence Skin-Ordner kopiert werden:

# cp integration/script-news.xml /usr/share/kodi/addon/skin.confluence/720p/

Die Datei "Custom_NewsCenter.xml" in den Confluence Skin-Ordner kopiert werden:

# cp integration/Custom_NewsCenter.xml /usr/share/kodi/addon/skin.confluence/720p/

Die Bilddateien aus dem integration Ordner in den Confluence Media Ordner kopieren:

# cp integration/*.png /usr/share/kodi/addon/skin.confluence/media/


2. Änderungen an der Datei Home.xml:
--------------------------------------------------
                        <control type="group" id="9001">
                                <left>0</left>
                                <top>70</top>
                                <onup>9000</onup>
                                <ondown>9002</ondown>
.
.
.
<!-- Start NewsCenter -->
                                <control type="grouplist" id="50506">
                                        <include>HomeSubMenuCommonValues</include>
                                        <onleft>9014</onleft>
                                        <onright>9014</onright>
                                        <visible>Container(9000).HasFocus(50505)</visible>
                                        <!-- Buttons for the grouplist -->
                                        <include>HomeSubMenuNews</include>
                                </control>
                        </control>
<!-- Ende NewsCenter -->

.
.
.
                <control type="group" id="9002">
                        <onup>9001</onup>
                        <ondown>20</ondown>
.
.
.
<!-- Start NewsCenter -->
                        <control type="fixedlist" id="50509">
                                <animation effect="slide" start="0,0" end="-91,0" time="0" condition="StringCompare(Container(703).NumItems,2) | StringCompare(Container(703).NumItems,4)">conditional</animation>
                                <visible>Container(9000).HasFocus(50505)</visible>
                                <onleft>703</onleft>
                                <onright>703</onright>
                                <onup>9001</onup>
                                <ondown>20</ondown>
                                <include>HomeAddonsCommonLayout</include>
                                <content>
                                        <include>HomeAddonItemsNews</include>
                                </content>
                        </control>
<!-- Ende NewsCenter -->

                        <control type="fixedlist" id="703">
                                <animation effect="slide" start="0,0" end="-91,0" time="0" condition="StringCompare(Container(703).NumItems,2) | StringCompare(Container(703).NumItems,4)">conditional</animation>
                                <visible>Container(9000).HasFocus(3)</visible>
                                <onleft>703</onleft>
                                <onright>703</onright>
                                <onup>9001</onup>
                                <ondown>20</ondown>
                                <include>HomeAddonsCommonLayout</include>
                                <content>
                                        <include>HomeAddonItemsMusic</include>
                                </content>
                        </control>

.
.
.
.
                                <content>
<!-- Start NewsCente -->
                                        <item id="50505">
                                                <label>50505</label>
                                                <onclick>ActivateWindow(4117)</onclick>
                                                <icon>-</icon>
                                                <thumb>-</thumb>
                                                <visible>!Skin.HasSetting(HomeMenuNoMovieButton) +  System.HasAddon(plugin.program.newscenter)</visible>
                                        </item>
<!-- Ende NewsCenter -->


                                        <item id="7">
                                                <label>31950</label>
                                                <onclick>ActivateWindow(Weather)</onclick>
                                                <icon>-</icon>
                                                <thumb>-</thumb>
                                                <visible>!Skin.HasSetting(HomeMenuNoWeatherButton) + !IsEmpty(Weather.Plugin)</visible>
                                        </item>

--------------------------------------------------



3. Änderungen an der Datei IncludesHomeMenuItems.xml:
--------------------------------------------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>
.
.
.
<!-- Start NewsCenter -->
        <include name="HomeSubMenuNews">
                <control type="image" id="50100">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3" flipx="true">HomeSubEnd.png</texture>
                </control>
                <control type="button" id="50115">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau in 100s</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.Tagesschau100), true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschau_100")</onclick>
                </control>
                <control type="button" id="50101">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.Tagesschau), true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschau")</onclick>
                </control>
                <control type="button" id="50118">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>MDR Aktuell 130s</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.NDRKompakt),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_mdr_aktuell_130")</onclick>
                </control>
                <control type="button" id="50119">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Kinder News</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.KinderNachrichten),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_kinder_nachrichten")</onclick>
                </control>
                <control type="button" id="50120">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>BR Rundschau 100s</label>
                        <visible>SubString(Window(Home).Property(NewsCenter.Visible.BRRundschau100),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_rundschau100")</onclick>
                </control>
                <control type="button" id="50121">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>NDR Aktuell kompakt</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.NDRKompakt),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_ndrkompakt")</onclick>
                </control>


                <control type="button" id="50116">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Feed Auswahl</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_select_dialog")</onclick>
                </control>
                <control type="button" id="50117">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Sport</label>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=show_buli_select")</onclick>
                </control>
                <control type="button" id="50102">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter in 60s</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.Wetter60),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetteronline")</onclick>
                </control>
                <control type="button" id="50103">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.WetterInfo),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetterinfo")</onclick>
                </control>
                <control type="button" id="561032">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Wetter.net</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.WetterNet),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_wetternet")</onclick>
                </control>
                <control type="button" id="561033">
                        <include>ButtonHomeSubCommonValues</include>
                        <label>Tagesschau Wetter</label>
                        <visible>SubString(Window.Property(NewsCenter.Visible.TagesschauWetter),true)</visible>
                        <onclick>RunScript(plugin.program.newscenter,"?methode=play_tagesschauwetter")</onclick>
                </control>


                <control type="image" id="90126">
                        <width>35</width>
                        <height>35</height>
                        <texture border="0,0,0,3">HomeSubEnd.png</texture>
                </control>
        </include>
<!-- Ende NewsCenter -->
--------------------------------------------------





4. Änderungen an der Datei IncludesHomeRecentlyAdded.xml:
--------------------------------------------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>
        <include name="HomeRecentlyAddedInfo">
                <control type="group" id="9003">
                        <onup>20</onup>
                        <ondown condition="System.HasAddon(script.globalsearch)">608</ondown>
                        <ondown condition="!System.HasAddon(script.globalsearch)">603</ondown>
                        <visible>!Window.IsVisible(Favourites)</visible>
                        <include>VisibleFadeEffect</include>
                        <animation effect="fade" time="225" delay="750">WindowOpen</animation>
                        <animation effect="fade" time="150">WindowClose</animation>


<!-- Start NewsCenter -->
                        <include>HomeRecentlyAddedNewsInfo</include>
<!-- Ende NewsCenter -->
--------------------------------------------------







5. Änderungen an der Datei includes.xml:
--------------------------------------------------
<?xml version="1.0" encoding="UTF-8"?>
<includes>
        <include file="defaults.xml" />
        <include file="ViewsVideoLibrary.xml" />
        <include file="ViewsMusicLibrary.xml" />
        <include file="ViewsFileMode.xml" />
        <include file="ViewsPictures.xml" />
        <include file="ViewsAddonBrowser.xml" />
        <include file="ViewsLiveTV.xml" />
        <include file="ViewsPVRGuide.xml" />
        <include file="ViewsWeather.xml" />
        <include file="IncludesCodecFlagging.xml" />
        <include file="IncludesHomeRecentlyAdded.xml" />
        <include file="script-tvhighlights.xml" />
<!-- Start NewsCenter -->
        <include file="script-news.xml" />
<!-- Ende NewsCenter -->
--------------------------------------------------



Parametrisierung bei Pluginaufrufes:
====================================
Wird das Plugin ohne Parameter gestartet, wird der Service auf "aktiv" gesetzt und die Daten passend zu den vorgenommenen Einstellungen werden in regelmäßigen Abständen aktualisiert.



XBMC.RunScript(plugin.program.newscenter,"?methode=start_service")
  Markiert den Service als aktiv, Daten werden geholt.

XBMC.RunScript(plugin.program.newscenter,"?methode=stop_service")
  Markiert den Service als gestoppt, es werden keine Daten mehr geholt.

Start und Stop Service ist nur im Skinnermode aktiv. Wenn Skinnermode nicht aktiviert wurde, lÃ¤uft immer ein Update
solange Content Refresh nicht auf 0 gesetzt ist.




XBMC.RunScript(plugin.program.newscenter,"?methode=play_tagesschau")
  Startet letzte Folge der Tagesschau

XBMC.RunScript(plugin.program.newscenter,"?methode=play_tagesschau_100")
  Startet letzte Folge der Tagesschau in 100 Sekunden

XBMC.RunScript(plugin.program.newscenter,"?methode=play_wetteronline")
  Startet aktuellen Wetterbericht in 60 Sekunden

XBMC.RunScript(plugin.program.newscenter,"?methode=play_wetterinfo")
  Startet aktuellen Wetterbericht von Meteogroup

XBMC.RunScript(plugin.program.newscenter,"?methode=play_kinder_nachrichten")
  Startet letzte Folge der Kinder Nachrichtensendung logo

XBMC.RunScript(plugin.program.newscenter,"?methode=show_select_dialog")
  Oeffnet Auswahlfendster fuer angezeigten Skin (switch ist temporär)

XBMC.RunScript(plugin.program.newscenter,"?methode=set_default_feed")
  Oeffnet Auswahlfendster fuer Default Feed (permanent)  

- show_select_dialog
- show_buli_select
- show_bulilist (benötigt Parameter buliliga=[1|2] & bulipage=[1|2]
- show_livestream_select_dialog


Methoden Auflistung:
====================


Dienst:
=======
methode=start_service
methode=stop_service
methode=set_skinmode
methode=unset_skinmode
methode=set_default_feed
methode=get_uwz_count
methode=refresh

Videos:
=======
methode=play_tagesschau
methode=play_tagesschau_100
methode=play_wetteronline
methode=play_wetterinfo
methode=play_wetternet
methode=play_tagesschauwetter
methode=play_kinder_nachrichten
methode=play_mdr_aktuell_130
methode=play_rundschau100
methode=play_ndraktuellkompakt

Livestreams:
============
methode=play_livestream_euronews
methode=play_livestream_ntv
methode=play_livestream_n24
methode=play_livestream_tagesschau24
methode=play_livestream_phoenix
methode=play_livestream_dw


Dialoge:
========
methode=show_select_dialog
methode=show_livestream_select_dialog
methode=show_buli_select
methode=show_bulilist
methode=show_bulispielplan
methode=show_bulinaechsterspieltag
methode=show_unwetter_warnungen


Container:
==========
methode=get_buli_spielplan_items
methode=get_buli_table_items
methode=get_buli_naechsterspieltag_items
methode=get_feed_items
methode=get_pollen_items
methode=get_unwetter_warnungen


Wetterkarten-Container:
=======================
methode=get_dwd_pics_base
methode=get_dwd_pics_base_uwz
methode=get_dwd_pics_extended
methode=get_dwd_pics_bundesland
methode=get_dwd_pics_bundesland_uwz
methode=get_dwd_pics_base_extended
methode=get_euronews_wetter_pics
methode=get_uwz_maps



Properties:
===========

LatestNews.Service                    - (active/inactive) Schaltet im Skinnermodus den Datenrefresh ein/aus

LatestNews.<nr>.Title                 - RSS Titel
LatestNews.<nr>.Desc                  - RSS Beschreibung
LatestNews.<nr>.Logo                  - RSS Bild
LatestNews.<nr>.Date                  - RSS Artikel Veröffentlichung
LatestNews.<nr>.HeaderPic             - RSS Provider Bild

NewsCenter.PLZ                        - Postleitzahl aus den Settings
NewsCenter.Bundesland                 - Ermitteltes Bundesland (von PLZ)

NewsCenter.Unwetter.Anzahl            - Anzahl Unwetterwarnungen
