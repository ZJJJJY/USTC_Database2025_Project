package com.book.backend.service;

import com.book.backend.common.R;
import com.book.backend.pojo.Comment;
import com.baomidou.mybatisplus.extension.service.IService;
import com.book.backend.pojo.dto.CommentDTO;
import com.book.backend.pojo.dto.ReplyDTO;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;

/**
 * @author 程序员小白条
 * @description 针对表【t_comment】的数据库操作Service
 * @createDate 2023-02-06 19:19:20
 */
public interface CommentService extends IService<Comment> {
    /**
     * 获取弹幕列表
     *
     * @return R<Comment>
     */
    R<List<CommentDTO>> getCommentList();

    /**
     * 添加弹幕
     *
     * @return R
     */
    R<String> addComment(CommentDTO commentDTO);

    R<String> replyComment(ReplyDTO replyDTO);
}
