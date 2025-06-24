package com.book.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.book.backend.pojo.Books;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

public interface BooksMapper extends BaseMapper<Books> {

    /**
     * 分页查询图书信息，并根据评分排序
     */
    List<Books> searchBookPageWithRating(@Param("page") Page<Books> page, @Param("condition") String condition, @Param("query") String query);

    @Select({
            "<script>",
            "SELECT COUNT(*)",
            "FROM t_books b",
            "<where>",
            "  <if test='condition != null and query != null'>",
            "    ${condition} LIKE CONCAT('%', #{query}, '%')",
            "  </if>",
            "</where>",
            "</script>"
    })
    int countBooksWithRating(@Param("condition") String condition, @Param("query") String query);
}
