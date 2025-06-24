package com.book.backend.pojo;

import lombok.Data;

import java.util.Date;

@Data
public class BookRating {
    private Long id;
    private String bookNumber;
    private String username;
    private Integer score;
    private Date createTime;
}
