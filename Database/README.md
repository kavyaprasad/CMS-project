# FeedMe CMS DataBase

## Contents

### 1. Entities

### 2. Relations and Columns

### 3. Others

## Entities

There are 2 core entities in the design: User and Video. The user entity manages users' information and their permissions for operations. The video entity and its accessory entities manage information relevant to videos. These two entities are connected both directly and indirectly.

Directly, each video is connected to a user, implementing the relationships of a-video-belongs-to-only-one-user and a-user-can-have-many-videos. 

Indirectly, the entity of Comment connects users to videos and vice versa ways.

Video's accessory entities are: 

1. timeMarker and videoTimeMarkerMapping;
2. ingredient and videoIngredientMapping;
3. taste and videoTasteMapping.

More of the functionalities and what information each table tracks is detailed in **Relations and Columns**

## Relations and Columns
### Relations

#### video and user
* Each video must belong to at least one user;
* Each user can have 0 or more videos;

#### video, user, and comment
* Each video can have 0 or more comments;
* Each user can have 0 or more comments;
* Each comment must belong to at least one video;
* Each comment must belong to at least one user;

#### video and time marker(tag)
* Each video can have 0 or more time markers(tags);
* Each time marker(tag) can belong to 0 or more videos;

#### video and ingredient
* Each video must have at least one ingredient;
* Each ingredient can belong to 0 or more videos;

#### video and taste
* Each video must have at least one taste;
* Each taste can belong to 0 or more videos;

### Columns
1. video and accessories

  1.1 video

      video table track the following information:

      a. title: video title

      b. duration: the length of time of a video

      c. price: null or 0 means free; otherwise user need to pay for the video (this is optional 
      and requires another mapping table between user and video, say a purchurse table with 
      video id, user id, and purchurse date)
      
      d. instruction: a text field that contains json format data; the json data has 2 field, 
      from_time and instruction; the from_time provides a time point indicating when its 
      cooresponding instruction should be displayed or be displayed in bold. A web-based tool 
      can be provided/implemented to help user convert their pure, unformatted instruction txt 
      into time-formatted instruction, something similar to lyrics.
      
      e. view count: every time a user starts playing a certain video, its view count ++;
      
      f. rating: default 0; this value will be updated periodically by a recommendation sub-system 
      that is not in the scope of current project. So we can just temporarily put in some fake score.
      
      g. suspended: if a video is reported to be inappropriate, we change this value to 1, meaning this 
      video is waiting for the admin to check if it is inapproriate as reported.
      
      h. suspended_date: records when the video is reported as inappropriate.
      
      i. deleted: since we only do soft deletion in the database (this is becasue we don't want 
      to lose track of the location of the actual video files in file system), if this field **is not null**, 
      it will display as "video is deleted" to users; when a admin decide to delete a video for whatever reason, 
      this field is assigned a datetime.
      
      j. created: the upload time of a video
      
      k. modified: records the most recent time when a user edits a video's information, such as adding/deleting 
      ingredient.

  1.2 time marker (tagging) system. 
  When user want to add a tag to a video, he can select from what is already in the time marker table; if his input is not there, first we need to insert it into time marker table, and then create a new record in the mapping table with an time marker id pointing to the record in time marker table.
  
    1.2.1 time marker (tag)
    
      a. content: records a tag
    
    1.2.2 video time_marker mapping
      
      a. video_id: records which video a tag belongs to
      
      b. time_point: records when in the video the tag word/words is mentioned; 
      this is optional for current project
      
      c. time_marker_id: the FK that points to a tag in time marker table 
      
      d. deleted: for soft deletion

  1.3 taste
  Works similar to tagging system.
    
    1.3.1 video taste mapping
  
  1.4 ingredient
  Works similarly to tagging system.
    1.4.1 video ingredient mapping
  
  1.5 video resolution
    
    1.5.1 video resolution table
    
      a. video_id: indicates which video the file belongs to
      
      b. resolution: indicates the resolution of the actual file
      
      c. file_path: indicates the location of the actual file. The actual files in file system should be
      stored in such format: **video_file_directory/video_title/720p.mp4**
2. user

  2.1 user table

      a.  username: a unique field; this should be validated in the front end; specifically, 
      when a user registers, after he inputs the username he wants, we should check is the 
      username is already in use; a ajax query process by a method checkUsername() in User 
      controller can handle this.
      
      b. encrpt_pw: does Django provides such function?
      
      c. first_name:
      
      d. last_name:
      
      e. email: required
      
      f. is_admin: a boolean column; 0 means regular user and 1 means admin; we are goint to 
      use this to check if user has permission to do admin operations. For such methods, we should
      implement beforeAction() method to check if a user is a admin and put it in the beginning 
      of every such opertaion/method.

3. comment
    
  3.1 comment table

      a. user_id: the FK that points to a user record
      
      b. video_id: the FK that points to a video record
      
      c. comment: the content of comment
      
      d. suspended: default 0; if one comment is reported as inappropriate, this field will be update as 1
      
      e. suspended_date: records when a comment is reported.
      
      f. created: we are going to use this information to display comments in order
