package com.book.backend.pojo.dto;

import com.book.backend.pojo.Comment;
import lombok.Data;

import java.io.Serializable;
import java.util.List;

/**
 * @author 程序员小白条
 */
@Data
public class CommentDTO implements Serializable {
    public Integer id;
    public String avatar;
    public String msg;
    public Integer time;
    public String barrageStyle;
    public String userName;
    //父类ID
    public Integer pId;

    private List<Comment> replies; // 子评论列表

}
