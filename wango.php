<?php
if ($_GET["cmd"]=="left") {
  exec("sudo python moveleft.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}
if ($_GET["cmd"]=="nudgeleft") {
  exec("sudo python nudgeleft.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="right") {
  exec("sudo python moveright.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}
if ($_GET["cmd"]=="nudgeright") {
  exec("sudo python nudgeright.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="forward") {
  exec("sudo python moveforward.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}
if ($_GET["cmd"]=="back") {
  exec("sudo python moveback.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="up") {
  exec("sudo python faceup.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="down") {
  exec("sudo python facedown.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="headleft") {
  exec("sudo python faceleft.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="headright") {
  exec("sudo python faceright.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="headleftnudge") {
  exec("sudo python faceleftnudge.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="headrightnudge") {
  exec("sudo python facerightnudge.py");
  //exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" image.jpg");
}

if ($_GET["cmd"]=="faceon") {
  exec("sudo rm turn_off_face.txt");
  exec("sudo python PiFace2.py &");
}

if ($_GET["cmd"]=="faceoff") {
  exec("sudo cp turn_off_face.txt2 turn_off_face.txt");
}

if ($_GET["cmd"]=="stop") {
  exec("sudo python stop.py");
}
if ($_GET["cmd"]=="run") {
  exec("sudo python run.py");
}

if ($_GET["cmd"]=="snap") {
  exec("sudo fswebcam -d v4l2:/dev/video0 -i 0 -r 320x240  --timestamp \"%Y-%m-%d %H:%M:%S\" /mnt/ramdisk/image.jpg");
}

if ($_GET["cmd"]=="startcam") {
  exec("sudo cp turn_off_face.txt2 turn_off_face.txt");
  exec("sudo python takepicture.py &");
}

if ($_GET["cmd"]=="stopcam") {
  exec("sudo rm turn_off_face.txt");
}

if ($_GET["cmd"]=="resetcam") {
  exec("sudo ./resetcam");
}

if ($_GET["cmd"]=="shutdown") {
  exec("sudo shutdown now");
}

if ($_GET["cmd"]=="reboot") {
  exec("sudo reboot &");
}

?>
