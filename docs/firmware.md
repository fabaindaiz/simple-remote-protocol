# Firmware

The firmware runs over circuitpython and is responsible for the communication with the client and the control of the hardware.

Firmware is separated in two main parts:

### Internal loader

It is responsible for the initial setup of the microcontroller and cannot be updated.
Because of that, it was designed to be as small as possible and rigurouslly tested.

The responsibilities of the internal loader are:

  - Initialize the network interface
  - Load the main firmware from the filesystem
  - Load the user application from the filesystem

### Main firmware

It is responsible for the communication with the client and update related features.
In case of update failure, the internal loader will load the original main firmware.

The responsibilities of the main firmware are:

  - Communication with the client using the protocol
  - Updates of the firmware and user application
  - System monitoring and commands execution

## User interaction

The user can interact with the firmware using the client application provided in this repository.
Connection is secured using AES-256-CTR encryption, and the user requires login with a password.

The client application can be used in two ways:

  - Using the command line interface to send simple commands and receive responses.
  - Using one of the provided scripts that automate more complex tasks like firmware update.
