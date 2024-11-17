select *,DATETIME(ROUND(booking_start / 1000), 'unixepoch') AS start, DATETIME(ROUND(booking_end / 1000), 'unixepoch') AS isodate_end from booking;


select * from booking where booked_item_id = 3 and 
    (booking_start <= '1735772400000' or booking_end >= '1735686000000') and 
    booking_status != 'CANCELLED'  ;


select * from booking where booked_item_id = 3 and 
    (booking_start BETWEEN '2024-11-20' AND '2024-11-21') or
    (booking_end BETWEEN '2024-11-20' AND '2024-11-21');

select * from booking where booked_item_id = 3 and 
    (booking_start BETWEEN 1731193200000 AND 1731193200000) or
    (booking_end BETWEEN 1731193200000 AND 1731193200000);

select * from booking where booked_item_id = 3 and 
    (booking_start BETWEEN 1735686000000 AND 1735858800000) or
    (booking_end BETWEEN 1735686000000 AND 1735858800000);


SELECT
    *
FROM
    BOOKING
WHERE
    BOOKED_ITEM_ID = 10
    AND BOOKING_STATUS != 'CANCELLED'
    AND ((BOOKING_START BETWEEN '1732921200000'
    AND '1734044400000')
    OR (BOOKING_END BETWEEN '1732921200000'
    AND '1734044400000'))