Inline::C vs perlxs
---------------------------------
In meinem letzten Post hab ich schon durchblicken lassen das ich mich aktuell vermehrt mit der Einbindung
von C Libarys nach perl beschäftige. Wer sich mit dem Thema beschäftigt wird ziemlich schnell auf die Offizielle
[perlxs](http://perldoc.perl.org/perlxs.html) doku stoßen. Als ich vor paar jahren das erste mal drüber geschaut
habe, hats mich vor lauter Doku fast erschlagen & bin schnell zu [Inline::C](http://search.cpan.org/~sisyphus/Inline-0.53/C/C.pod) gewechselt.

C Libarys in Perl
-------------------

Ich bin immer wieder erstaunt wie umfangreich das cpan archiv ist & hab auf anhieb nicht viele Libarys
gefunden die noch nicht nach perl portiert wurden. Jedoch bin ich auf [Hotpatch](https://github.com/vikasnkumar/hotpatch) gestoßen.

Ich werde mich die nächsten Tage also ranmachen & nach und nach das Modul nach [Inline::C](http://search.cpan.org/~sisyphus/Inline-0.53/C/C.pod) und [perlxs](http://perldoc.perl.org/perlxs.html) zu portieren.



[Inline::C](http://search.cpan.org/~sisyphus/Inline-0.53/C/C.pod)
----------

Variante Inline geht ziemlich schnell von der Hand, wie am beispiel unten gezeigt

` use Inline C => Config =>
               ENABLE => AUTOWRAP =>
               LIBS => "-lhotpatch ";`

Mit der Headline defnieren wir die Libary und das Autowrap für das prototypen bzw "variablen convertierung" zwischen perl & c.

`use Inline C => <<'END_OF_C_CODE';`

Defeniert den beginn der C-functionen. Der Rest ist reihner C Code 

{% gist 6502495 %}



Example 
----------

Ich glaub dazu muss ich keine großen worte verlieren ;)

{% gist 6502621 %}


Die Tage mehr zu Vor & Nachteilen sowie die portierung nach perlxs