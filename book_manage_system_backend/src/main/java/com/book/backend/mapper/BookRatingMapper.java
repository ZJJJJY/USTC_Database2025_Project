package com.book.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.book.backend.pojo.BookRating;
import org.apache.ibatis.annotations.Param;

public interface BookRatingMapper extends BaseMapper<BookRating> {
    int insertOrUpdate(BookRating rating);
}
