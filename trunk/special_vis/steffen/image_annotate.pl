#!/usr/bin/env perl

# $Id$

use warnings;
use strict;

use Getopt::Long;
use Image::Magick;

my $movie_title = "SimTitle";
my $max_frames = 201;

my $result = GetOptions(
    "title=s" => \$movie_title,
    "max_frames=i" => \$max_frames,
);

my ($text_width, $text_height);
my $font = 'CenturySchl-Roma';
my $text_buffer_x = 5;
my $text_buffer_y = -8;
my @font_metrics;

for (my $frame_num=0; $frame_num<$max_frames; $frame_num++) {
    my $in_filename = sprintf("frame_%04d.tga", $frame_num);
    my $out_filename = sprintf("frame_%04d_ann.tga", $frame_num);

    # get the file
    print "Reading $in_filename\n";
    my $image = new Image::Magick;
    $image->Read($in_filename);

    # get image dimensions
    my $image_height = $image->Get('height');
    my $image_width = $image->Get('width');

    # put a title on it
    @font_metrics = $image->QueryFontMetrics(
	text => $movie_title,
	pointsize => 26,
	font => $font,
    );
    my $movie_title_text_height = $font_metrics[5];

    $image->Annotate(
	text => $movie_title,
	font => $font,
	pointsize => 26,
	stroke => 'white',
	fill => 'white',
	align => 'Center',
	x => int $image_width/2,
	y => $movie_title_text_height + $text_buffer_y - 5,
    );

    # put on it who made the data
    my $info_text = "Steffen Abe";
    @font_metrics = $image->QueryFontMetrics(
	text => $info_text,
	pointsize => 20,
	font => $font,
    );
    my $info_text_height = $font_metrics[5];

    $image->Annotate(
	text => $info_text,
	font => $font,
	pointsize => 20,
	stroke => 'white',
	fill => 'white',
	x => $text_buffer_x,
	y => $info_text_height + $text_buffer_y,
    );

    # put on it who did the visualisation
    my $vis_text = 'Visualisation: Paul Cochrane: paultcochrane@gmail.com';
    $image->Annotate(
	text => $vis_text,
	font => $font,
	pointsize => 14,
	stroke => 'white',
	fill => 'white',
	align => 'Center',
	x => int $image_width/2,
	y => $image_height-13,
    );

    # determine the width of the frame number info text
    my $frame_num_point_size = 18;
    if ($frame_num == 0) {
	my $frame_num_text = sprintf("frame: %03d", 0);
	my @font_metrics = $image->QueryFontMetrics(
	    text => $frame_num_text,
	    pointsize => $frame_num_point_size,
	    font => $font,
	);
	$text_width = $font_metrics[4];
	$text_height = $font_metrics[5];
    }

    # put the frame number in the top right hand corner
    my $frame_num_text = sprintf("frame: %03d", $frame_num);
    $image->Annotate(
	text => $frame_num_text,
	font => $font,
	pointsize => $frame_num_point_size,
	stroke => 'white',
	fill => 'white',
	x => $image_width - $text_width - $text_buffer_x,
	y => $text_height + $text_buffer_y,
    );

    # write out the result
    $image->Write($out_filename);
    print "Wrote $out_filename\n";
}

