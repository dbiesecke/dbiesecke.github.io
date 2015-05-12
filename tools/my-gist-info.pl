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
    printf "%s: %s\n", $row->{name}, $row->{description} || 'no description';
}

print "---------------------------- GIST's ----------------\n\n";
print "[Notes]()\n\n";
    my $special;
   my $g = Pithub::Gists->new;
    $result = $g->list( user => 'dbiesecke' );
    if ( $result->success ) {
        while ( my $row = $result->next ) {
            #print Dumper($row)."\n";
#            printf "   * [%s](%s)\n", $row->{description},$row->{html_url} || 'no description';
            my $files = $row->{files};
             foreach my $file ( keys $files )  {
                   next if not ($file =~/README.md/);
#                   print Dumper($file)."\n";    
            printf "   * [%s](%s)\n", $row->{description},$row->{html_url}."/raw/README.md" || 'no description';

             }
        }
    }
