# Overview
This project was created by Caleb Jones, Brandon Woodward, Zachary Cox, and Emmet Larson as a submission for the 2024 York College of Pennsylvania Hackathon. The theme of the event was 'Matrix' and our team decided we wanted to create a USB device that can scrape files off a computer and remotely upload them to a web server which we hosted on a local network. The contents of the project were demonstrated in a controlled environment with consent of those whose computers we used the device on. That being said, we do not endorse the use of this software/hardware for illegal activities, nor are we responsible for individuals who do as such. This document will server as an overview of what our project is and how we implemented the above features.

# The Device
Our implementation used a [Raspberry PI Zero 2 W](https://www.microcenter.com/product/643085/raspberry-pi-zero-2-w) and a Micro USB -> USB Type A device to interface with the computer. This device was selected for a multitude of reasons, though any PI device which has OTG and a wireless network chip would work as well. Namely, the PI Zero 2 W is extremely small, and could be convincingly disguised as a USB flash drive. For the casing, we [3D printed](https://cults3d.com/en/3d-model/gadget/m-n-mal-raspberry-pi-zero-2-case-housing-sleeve). To interface with the device, we used the Putty software which allows you to plug the IP of the PI device in and directly interface with the console of the PI. This allowed us to write our scripts directly on the PI remotely from our devices.

Not only did using Putty allow us to remotely code on the PI device, but it also allowed us to execute commands remotely on the device (will be important later). One issue we ran into around this point in the project is once the PI is plugged into the victim's computer, how do we get the files off and into our web server? Our workaround for this used the PI Zero's OTG feature, which allows the device to be recognized as a variety of other USB devices. We figured that the easiest way would be to have OTG make the victim computer recognize our PI Zero as a keyboard, that way we can send commands to the PI Zero to press certain keys in a specific order, and through the Windows CMD send the desired files to our web server.

To get the CMD to send the files to our computer, we opted to use inline code execution. For the purpose of this project, we did not forcibly install python on the victim computer, but for an actual implementation of such a device, that would be the first step. As the CMD allows a user to directly run code inline, all a keyboard would have to do is type: "python exec(*script you want to execute*)". We created two scripts for the CMD to execute, one which creates a background animation using the [Pygame](https://www.pygame.org/docs/) library. The second is the scraper, which navigates to a **predetermined** file path in the victims computer. A real implmentation of this device would have to automatically navigate to the correct folder using a recursive navigation library such as [Glob](https://docs.python.org/3/library/glob.html). The script then gets a reference to all the files of a certain extension (in our case, we chose .txt), connects to our web server, and uploads each file. As a little joke, we then have the script open notepad and write a little message for the victim; this was really as a proof of concept that an implementation of this could really do nearly *anything* that a regular user could do using a keyboard.

The Python file that we exectued on the PI is included above in the repository, but I will give a brief 
<p align="center">
  <img src="https://github.com/user-attachments/assets/acb5e248-bbe9-4483-8fc7-2eb36004d4da" />
</p>
