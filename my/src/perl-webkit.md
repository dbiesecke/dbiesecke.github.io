Webkit statisch in perl
========================================

Ich hab mich letzter zeit vermehrt mit Webkit beschäftigt & wollte es meinen Vorlieben entsprechend in ruby oder perl verwenden.
Dabei stieß ich auf so einige stolpersteine besonders mit den ständig wechselnden gtk webkit versionen.


Webkit Module - Getest & durchgefallen:
-------------------------

1. [WWW::WebKit](http://search.cpan.org/~nine/WWW-WebKit-0.05/lib/WWW/WebKit.pm)... Perl Modul
... aufgrund der nötigen Gtk3 Webkit libarys lies es sich auf vielen default server systemen nur mit massig balast installieren

2. [capybara-webkit](https://github.com/thoughtbot/capybara-webkit)... Ruby Modul
... dank guten gems läst es sich mit den default packetmanagern easy installieren, aber dummerweise nur schwer statische binarys bauen.
... desweiteren für meine ansprüche schon fast einwenig zu überladen & abstrakt, aber das is wohl geschmackssache.


[perl-qtwebkit](https://github.com/natedat/perl-qtwebkit) & [staticperl](http://search.cpan.org/~mlehmann/App-Staticperl-1.43/bin/staticperl)
-----------------------------------------------------------------------------------------------------------------------------------------

Da mein hauptaugenmerk dabei auf portabilität lag, bin ich am ende bei [QtWebkit](http://qt-project.org/doc/qt-5.0/qtwebkit/qtwebkit-module.html) gelandet.
Per Github bin ich auch prompt auf nen perl module gestoßen das es per XS einbindet, perfekt auch für [staticperl](http://search.cpan.org/~mlehmann/App-Staticperl-1.43/bin/staticperl).


Bin eigentlich kein Freund von JavaScript, aber wenns um DOM handling in HTML geht, ist es wahrlich unschlagbar, daher lassen sich auch noch so Ajax lastige HTTP Services ansprechen & easy verarbeiten.
Grund genug sich mal näher mit dem spartanisch dokumentierten source zu beschäftigen. 

Beim debuggen greif ich immer gerne auf proxys zum debuggen zurück, leider war keine möglichkeit gegeben, nen proxy
hinzuzufügen. Grund genug ein wenig am modul zu hacke :)

Somit entstand mein fork mit na neen "useTor" function die als proxy nen socks5 localhost mit port 9050 verwendet.
Module ist wie immer in meinem Repo.

{% gist 6444046 %}


