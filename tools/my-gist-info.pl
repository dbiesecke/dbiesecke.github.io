#!/usr/bin/env perl

use strict;
use warnings;
use Pithub::Repos;
use Pithub::Gists;

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
    printf "%s: %s\n", $row->{name}, $row->{description} || 'no description';
}

print "---------------------------- GIST's ----------------\n\n";
print "[Notes]()\n\n";

   my $g = Pithub::Gists->new;
    $result = $g->list( user => 'dbiesecke' );
    if ( $result->success ) {
        while ( my $row = $result->next ) {
            printf "   * [%s](%s)\n", $row->{description},$row->{html_url} || 'no description';
        }
    }
