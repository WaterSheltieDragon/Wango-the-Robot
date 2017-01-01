<?php

$movement_cmd_list = array("moveleft","nudgeleft","moveright","nudgeright","moveforward","moveback","stop","run", "faceup","facedown","faceleft","faceright", "faceleftnudge", "facerightnudge");

function writeCmd($channel) {
  $myfile = fopen("/mnt/ramdisk/cmd-".$channel.".txt", "w") or die("skipping cmd file.");
  fwrite($myfile, ".");
  fclose($myfile);
}

if (in_array($_GET["cmd"], $movement_cmd_list)) {
  writeCmd($_GET["cmd"]);
}

if ($_GET["cmd"]=="faceon") {
  exec("sudo rm turn_off_face.txt");
  exec("sudo python PiFace2.py &");
}

if ($_GET["cmd"]=="faceoff") {
  exec("sudo cp turn_off_face.txt2 turn_off_face.txt &");
}

if ($_GET["cmd"]=="snap") {
  exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" /mnt/ramdisk/image.jpg &");
}

if ($_GET["cmd"]=="startcam") {
  exec("sudo cp turn_off_face.txt2 turn_off_face.txt");
  exec("sudo python takepicture.py &");
}

if ($_GET["cmd"]=="stopcam") {
  exec("sudo rm turn_off_face.txt &");
}

if ($_GET["cmd"]=="resetcam") {
  exec("sudo ./resetcam &");
  exec("sudo ./resetservos &");
}

if ($_GET["cmd"]=="shutdown") {
  exec("sudo shutdown now &");
}

if ($_GET["cmd"]=="reboot") {
  exec("sudo reboot &");
}

?>
