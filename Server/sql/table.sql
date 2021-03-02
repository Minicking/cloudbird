create table if not exists user(
	id int unsigned auto_increment primary key,
	name varchar(20) not null,
	account varchar(20) not null unique,
	password varchar(100) not null,
	email varchar(50) not null,
	regDate datetime not null default '2020-5-1 00:00:00',
	lastDate datetime not null default '2020-5-1 00:00:00',
	lastIP varchar(25) not null default '0.0.0.0',
	certification boolean default false,
	login boolean default false
)engine=innodb default charset=utf8;
create table if not exists confirmcode(
	id int unsigned auto_increment primary key,
	email varchar(50) not null,
	code char(5) not null,
	regDate datetime not null
)engine=innodb default charset=utf8;
create table if not exists friend(
	id int unsigned auto_increment primary key,
	owner int unsigned not null,#此条好友数据的所有者
	target int unsigned not null,#此条好友数据指向的好友
	addData datetime default '2020-5-1 00:00:00',#添加好友的时间
	state int unsigned not null default 0,#此条好友数据的状态，如特别关心
	constraint owner_FK foreign key(owner) references user(id) on delete cascade on update cascade,
	constraint target_FK foreign key(owner) references user(id) on delete cascade on update cascade
)engine=innodb default charset=utf8;
create table if not exists friendrequest(
	id int unsigned auto_increment primary key,
	requester int unsigned not null,
	target int unsigned not null,
	requestDate datetime default '2020-5-1 00:00:00',#添加好友的时间
	constraint fr_requester_FK foreign key(requester) references user(id) on delete cascade on update cascade,
	constraint fr_target_FK foreign key(target) references user(id) on delete cascade on update cascade
)engine=innodb default charset=utf8;