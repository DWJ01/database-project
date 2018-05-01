insert into airline values("China Eastern");
insert into airline values("Emirates");
insert into airline values("Hokkaido");
insert into airline values("Hawaiian");
insert into airline values("Air Canada");

insert into airport values("JFK", "NYC");
insert into airport values("PVG", "Shanghai");
insert into airport values("HNL", "Hawaii");
insert into airport values("HND", "Tokyo");
insert into airport values("SYD", "Sydney");

insert into airline_staff values ("JP", "jt1997", "Jack", "Paul", "1997-12-23", "China Eastern");
insert into airline_staff values("BO", "ab9607", "Ben", "Ohno", "1996-07-25", "Emirates");
insert into airline_staff values("MJ", "lo520", "Jun", "Matsumoto", "1983-08-30", "Hokkaido");

insert into airplane values ("China Eastern", 48, 100);
insert into airplane values ("China Eastern", 46, 2000);
insert into airplane values ("Emirates", 788, 5000);
insert into airplane values ("Hokkaido", 520, 7000);
insert into airplane values ("Hawaiian", 899, 6000);
insert into airplane values ("Air Canada", 65, 9000);

insert into flight values ("China Eastern", 8925, "JFK", "2017-12-30 15:10:00","PVG", "2017-12-30 19:00:00", 200, "upcoming", 48);
insert into flight values ("China Eastern", 6524, "PVG", "2018-12-05 17:00:00", "JFK", "2018-12-06 07:20:00", 300, "in-progress", 46);
insert into flight values ("Emirates", 6213, "HNL", "2016-09-02 09:00:08", "JFK", "2016-09-02 12:57:00", 100, "delayed", 788);
insert into flight values ("Hokkaido", 7892, "SYD", "2018-03-25 08:50:00", "HND", "2018-03-25 16:00:00", 900, "in-progress", 520);
insert into flight values ("Hawaiian", 9843, "HNL", "2018-02-14 07:08:00", "JFK", "2018-02-15 09:00:00", 7000, "upcoming", 899);
insert into flight values ("Air Canada", 7621, "PVG", "2019-01-01 13:00:00", "SYD", "2019-01-01 15:00:00", 999, "delayed", 65);

insert into customer values("wf541@nyu.edu", "Cheryl Feng", "WF19971205", '7', "Sujin", "Suzhou", "Jiangsu", 13004507845, 'ab541', "2020-07-01", "China", "1997-12-23");
insert into customer values ("hl2679@nyu.edu", "Tiffany Li", "Lihuilin19970922", '9', "Shiji Avenue", "Shanghai", "Shanghai", 13001296766, 'cd2679', "2030-07-01", "America", "1997-09-22");
insert into customer values("mj0830@nyu.edu", "Jun Matsumoto", "mj19830830love", '3', "Johnnys", "tokyo", "Tokyo", 13912056455, 'ef890076', "2900-08-02", "Japan", "1983-08-30");
insert into customer values("os1024@nyu.edu", "Ohno Satoshi", "ohno19811024love", '7', "Johnnys", "tokyo", "Tokyo", 13452634117, 'gh78342', "2900-08-02", "Japan", "1981-10-24");
insert into customer values("ss0125@nyu.edu", "Sho Sakurai", "sho19820125love", '5', "Johnnys", "tokyo", "Tokyo", 13562489100, 'op67532', "2900-08-02", "Japan", "1982-01-25");
insert into customer values("am1224@nyu.edu", "Aiba Masaki", "aiba19821224love", '4', "Johnnys", "tokyo", "Tokyo", 13426753890, 'qr78234', "2900-08-02", "Japan", "1982-12-24");
insert into customer values("nk0617@nyu.edu", "Ninomiya", "nino19830617love", '3', "Johnnys", "tokyo", "Tokyo", 13567821904, 'yz67234', "2900-08-02", "Japan", "1983-06-17");

insert into ticket values (1997, "China Eastern", 8925);
insert into ticket values (2018, "China Eastern", 6524);
insert into ticket values (5876, "Emirates", 6213);
insert into ticket values (5200, "Hokkaido", 7892);
insert into ticket values (5626, "Hawaiian", 9843);
insert into ticket values (7889, "Air Canada", 7621);

insert into booking_agent values("kk51@nyu.edu", "kinkikids520", 519);
insert into booking_agent values("sz678@nyu.edu", "sexyzone782", 678);

insert into purchases values (1997,  "mj0830@nyu.edu", null, "2007-08-30");
insert into purchases values (2018, "am1224@nyu.edu", 519, "2017-06-17");
insert into purchases values (5876, "wf541@nyu.edu", 678, "2018-03-27");