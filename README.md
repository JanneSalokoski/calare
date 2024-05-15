# Calare

Calare is a calendar system for booking resources, for example meeting rooms or equipment.

Current version is 0.0.0.

## Features

Main features of Calare are:
- Easily add and customize _resources_
- Group resources into _collections_
- _View_ the _bookings_ of a resource or a collection
- Restrict the access of what information each _user_ can see with _access groups_
- Print out a _contract_ for a booking

### Resources

A resource is something you can book. It can be a meeting room of your office,
a football of your school class or a shared car of your friend group, for example.

Resources can have certain time periods when they are available.
They can have default booking options and different possible options.

### Collections

A collection is a group of resources. You could group all the badminton fields
of a sports center into one collection and all the swimming tracks into another.

You can have default options set for all the resources of a collection.

### Views

A view shows the bookings of a resource or a collection during a certain time period
for the user. There is a resource-view and a collection-view,
and you can view either a day, a week or a month at a time.

### Bookings

A booking is a reservation of a resource or multiple resources for a certain time period.
Depending on your configuration, the bookings can be created and modified by certain
access groups, moderated and accepted by other access groups and requested for by others.
The information of a booking can be hidden from an access group partially based on your configuration.

For example you could have all of your companies employees see if the meeting room is
reserved or not, but not who has reserved them. They could request bookings for rooms.
Managers could be allowed to see who has booked which room, but they couldn't edit
the bookings of others than themselves. Managers could accept bookings and create them.
Only location administrators could see all the information, edit bookings and delete them.

These can be configured on a per resource or collection basis.

### Users

A user is someone who is using Calare. There can be quest users and various access groups
of authenticated users. Users can have different permissions and capabilities based on
their access group.

### Access groups

An access group is a set of permissions that the users in the access group have.
A system administrator always has all the permissions, a quest user could have no permissions at all
and other access groups can have varying levels of access to the information stored.

### Contract

A contract contains infomration about the resource, the conditions it is being booked with,
the responsibilites of both the booker and the resource owner. The contract can be modified
by the owners of the resource and printed as a pdf-file to signed.

## Feature completion

- [ ] Backend
    - [ ] Database for storing information
    - [ ] Authentication
    - [ ] Creating and modifying bookings
    - [ ] Creating and modifying resources
    - [ ] Creating and modifying collections
    - [ ] Creating and modifying users
    - [ ] Creating and modifying access groups
    - [ ] Creating and modifying contracts
- [ ] User interface
    - [ ] Resource view
        - [ ] Day view
        - [ ] Week view
        - [ ] Month view
    - [ ] Collection view
        - [ ] Day view
        - [ ] Week view
        - [ ] Month view
    - [ ] Booking view
    - [ ] User view
    - [ ] Admin view
- [ ] Other
    - [ ] Installation package
    - [ ] Installation guide
    - [ ] Usage manual

## Installation

How to install a Calare instance

## Configuration

How to configure Calare


