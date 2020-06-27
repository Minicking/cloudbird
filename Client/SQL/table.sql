create table if not exists friend(
	id int unsigned auto_increment primary key,
	owner int unsigned not null,#此条好友数据的所有者
	target int unsigned not null,#此条好友数据指向的好友
	addData datetime default '2020-5-1 00:00:00',#添加好友的时间
	state int unsigned not null default 0,#此条好友数据的状态，如特别关心
	constraint owner_FK foreign key(owner) references user(id) on delete cascade on update cascade,
	constraint target_FK foreign key(owner) references user(id) on delete cascade on update cascade
)engine=innodb default charset=utf8;