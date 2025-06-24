package com.book.backend.pojo.dto;

import lombok.Data;

@Data
public class Reply {
    private String id;
    private String parentId; // 对应主评论 ID
    private String msg;
    private String userName;
}
