package com.book.backend.pojo.dto;

import lombok.Data;

@Data
public class RatingDTO {
    private String bookNumber; // 图书编号
    private Integer score;     // 评分（0~10）
    private String username;   // 用户名
}
