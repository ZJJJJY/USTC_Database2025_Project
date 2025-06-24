package com.book.backend.pojo.dto;


import lombok.Data;

@Data
public class ReplyDTO {
    private String parentId; // 父级评论ID
    private String msg;      // 回复内容
    private String userName;// 回复人用户名
}
