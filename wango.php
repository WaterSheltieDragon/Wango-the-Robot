<?php
// channel 1 is for the DC motors
$movement_cmd_list_1 = array("left","nudgeleft","right","nudgeright","forward","back","stop","run");
// channel 2 is for the Servo motors
$movement_cmd_list_2 = array("up","down","headleft","headright", "headleftnudge", "headrightnudge","headcenter");

function writeCmd($channel, $cmd) {
  $myfile = fopen("/etc/ramdisk/cmd".$channel.".txt", "w") or die("skipping cmd file.");
  fwrite($myfile, $cmd);
  fclose($myfile);
}

if (in_array($_GET["cmd"], $movement_cmd_list_1)) {
  writeCmd(1,$_GET["cmd"]);
}
if (in_array($_GET["cmd"], $movement_cmd_list_2)) {
  writeCmd(2,$_GET["cmd"]);
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
}

if ($_GET["cmd"]=="shutdown") {
  exec("sudo shutdown now &");
}

if ($_GET["cmd"]=="reboot") {
  exec("sudo reboot &");
}

?>
