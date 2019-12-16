<?xml version="1.0" encoding="UTF-8"?>
<window>
    <coordinates>
        <left>635</left>
        <top>180</top>
    </coordinates>
    <controls>
        <control type="group">
            <control type="image">
                <description>Background Image</description>
                <posx>0</posx>
                <posy>0</posy>
                <width>650</width>
                <height>720</height>
                <texture border="2">Background/loguploader-dialog-bg.png</texture>
            </control>
            <control type="image">
                <description>Dialog Header image</description>
                <posx>0</posx>
                <posy>0</posy>
                <width>650</width>
                <height>50</height>
                <texture colordiffuse="ffd73229" border="2">Background/loguploader-white.png</texture>
            </control>
            <control type="label" id="101">
                <description>header label</description>
                <posx>0</posx>
                <posy>0</posy>
                <width>650</width>
                <height>50</height>
                <font>font13</font>
                <label></label>
                <align>center</align>
                <aligny>center</aligny>
                <shadowcolor>FF000000</shadowcolor>
            </control>
            <control type="textbox" id="102">
                <left>20</left>
                <top>60</top>
                <width>610</width>
                <height>80</height>
                <font>font12</font>
                <align>left</align>
                <aligny>top</aligny>
                <label>Since this is your First Run of the Wizard, Would you like to Enable any of the following Settings?</label>
            </control>
        </control>
        <control type="grouplist" id="9000">
            <left>20</left>
            <top>140</top>
            <width>610</width>
            <height>520</height>
            <itemgap>-3</itemgap>
            <align>top</align>
            <orientation>vertical</orientation>
            <onup>201</onup>
            <ondown>201</ondown>
            <onleft>201</onleft>
            <onright>201</onright>
            <control type="radiobutton" id="301">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Trakt</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="302">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Real Debrid</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="303">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Login Data</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="304">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Sources.xml</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="305">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Profiles.xml</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="306">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My AdvancedSettings.xml</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="307">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Favourites.xml</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="308">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Super Favourites</label>
                <font>font12</font>
                <texturefocus colordiffuse="FF12B2E7">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="309">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Repositories</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="310">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Keep My Whitelist</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="311">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Clear Cache on Startup</label>
                <font>font12</font>
                <texturefocus colordiffuse="FF12B2E7">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="312">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Clear Packages on Startup</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
            <control type="radiobutton" id="313">
                <width>610</width>
                <height>40</height>
                <textwidth>565</textwidth>
                <textoffsetx>10</textoffsetx>
                <radioheight>45</radioheight>
                <radioposx>530</radioposx>
                <label>Clear Old Thumbnails on Startup</label>
                <font>font12</font>
                <texturefocus colordiffuse="ffd73229">RadioButton/MenuItemFO.png</texturefocus>
                <texturenofocus>RadioButton/MenuItemNF.png</texturenofocus>
                <textureradioonfocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonfocus>
                <textureradioonnofocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioonnofocus>
                <textureradioofffocus colordiffuse="ffd73229">RadioButton/radiobutton-focus.png</textureradioofffocus>
                <textureradiooffnofocus>RadioButton/radiobutton-nofocus.png</textureradiooffnofocus>
            </control>
        </control>
        <control type="group" id="9001">
            <control type="button" id="201">
                <left>350</left>
                <top>630</top>
                <width>300</width>
                <height>90</height>
                <font>font13</font>
                <textcolor>FFF0F0F0</textcolor>
                <label>Continue</label>
                <align>center</align>
                <aligny>center</aligny>
                <onup>9000</onup>
                <ondown>9000</ondown>
                <texturefocus border="40" colordiffuse="ffd73229">Button/loguploader-dialogbutton-fo.png</texturefocus>
                <texturenofocus border="40">Button/loguploader-dialogbutton-nofo.png</texturenofocus>
            </control>
        </control>
    </controls>
</window>
