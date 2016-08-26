#!/usr/bin/env perl

# use strict;
# use warnings;
use Pithub::Repos;
use Pithub::Gists;
use LWP::Simple;
use Data::Dumper;
# my $s = Pithub::Repos::Starring->new;
# my $stars = $s->list_repos(
#     user => 'dbiesecke',
# );
# if ( $stars->success ) {
#     while ( my $row = $stars->next ) {
#             my ($user,$desc,$lang) = ($row->{name},$row->{description},$row->{language});
#           printf "[%s][%s]\t\t%s \n", $row->{name}, $row->{language},$row->{description};
           
#             my $result = Pithub::Repos::Releases->new->list( user => $row->{owner}->{login}, repo => $row->{name},  );

#             unless ( $result->success ) {
#                 printf "something is fishy: %s\n", $result->response->status_line;
#                 exit 1;
#             }
            
#             while ( my $row = $result->next ) {
#                 printf "%s\n", $row->{name};
#                 print Dumper($row)."\ņ";
#                 sleep(1);
#             }      
#             # my $releases = Pithub::Repos::Releases->new->list(
#             #     repo  => $row->{name},
#             #     user  => $row->{user},
#             # );
#             # if($releases->success ) {
#             #      while ( my $rls = $releases->next ) {
#             #          print Dumper $rls;
#             #     }
#             # }
#         # print $row->{'full_name'}."\n";
#       # exit;
#         # next if not ($row->{files}->{'README.md'});
#         #print Dumper( $row->{files}->{'README.md'})."\n";
#         #$nav .= "   * [".$row->{description}."](/#!".$row->{files}->{'README.md'}->{raw_url}.")\n";
    
#     }
# }
#print Dumper($stars)."\n";
# exit;
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