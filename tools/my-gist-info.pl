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
    my $navrepo = "[Sources]()\n\n";
while ( my $row = $result->next ) {
#    printf "%s: %s\n", $row->{name}, $row->{description} || 'no description';
            #next if not ($row->{files}->{'README.md'});

            $navrepo .= "   * [".$row->{name}."](".$row->{clone_url}.")\n";

}

print "---------------------------- GIST's ----------------\n\n";

    my $nav = "[Gists]()\n\n";
    my $overview = "";
   my $g = Pithub::Gists->new;
    $result = $g->list( user => 'dbiesecke' );
    if ( $result->success ) {
        while ( my $row = $result->next ) {
            next if not ($row->{files}->{'README.md'});
            #print Dumper( $row->{files}->{'README.md'})."\n";
            $nav .= "   * [".$row->{description}."](/#!".$row->{files}->{'README.md'}->{raw_url}.")\n";

        }
    }

print $nav."\n\n".$navrepo."\n\n";
#print $overview."\n";