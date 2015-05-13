#!/usr/bin/env perl

use strict;
use warnings;
use Pithub::Repos;
use Pithub::Gists;
use LWP::Simple;
use Data::Dumper;


my $r = Pithub::Repos->new(
    per_page        => 100,
    auto_pagination => 1,
);
my $result = $r->list( user => 'dbiesecke' );

unless ( $result->success ) {
    printf "something is fishy: %s\n", $result->response->status_line;
    exit 1;
}

while ( my $row = $result->next ) {
#    printf "%s: %s\n", $row->{name}, $row->{description} || 'no description';
}

print "---------------------------- GIST's ----------------\n\n";

    my $nav = "[Notes]()\n\n";
    my $overview = "";
   my $g = Pithub::Gists->new;
    $result = $g->list( user => 'dbiesecke' );
    if ( $result->success ) {
        while ( my $row = $result->next ) {
            next if not ($row->{files}->{'README.md'});
            #print Dumper( $row->{files}->{'README.md'})."\n";
            $nav .= "   * [".$row->{description}."](".$row->{'html_url'}.")\n";
            my $cont = get($row->{files}->{'README.md'}->{raw_url});
             $cont =~ s/=//ig;
             $overview .= $row->{description}."\n------------------------\nHint:".$row->{name}."\n$cont\n\n\n\n\n\n";

        }
    }

print $nav."\n\n".$overview."\n";