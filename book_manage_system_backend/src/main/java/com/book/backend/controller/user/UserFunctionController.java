package com.book.backend.controller.user;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.book.backend.common.BasePage;
import com.book.backend.common.R;
import com.book.backend.pojo.*;
import com.book.backend.pojo.dto.CommentDTO;
import com.book.backend.pojo.dto.RatingDTO;
import com.book.backend.pojo.dto.ReplyDTO;
import com.book.backend.pojo.dto.ViolationDTO;
import com.book.backend.service.*;
import com.book.backend.utils.JwtKit;
import io.swagger.annotations.ApiOperation;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @author 程序员小白条
 */
@RestController
@RequestMapping("/user")
public class UserFunctionController {
    @Resource
    private BooksService booksService;
    @Resource
    private BookRuleService bookRuleService;
    @Resource
    private NoticeService noticeService;
    @Resource
    private UsersService usersService;
    @Resource
    private BooksBorrowService booksBorrowService;
    @Resource
    private ViolationService violationService;

    @Resource
    private CommentService commentService;
    @Resource
    private AiIntelligentService aiIntelligentService;

    @Resource
    private JwtKit jwtKit;
    /**
     * 图书查询 分页和条件查询 (模糊查询)
     *
     * @param basePage 用于接受分页传参
     * @return R<Page < Books>>
     */
    @PostMapping("/search_book_page")
    @ApiOperation("图书查询 分页和条件查询")
    public R<Page<Books>> searchBookPage(@RequestBody BasePage basePage) {
        return booksService.searchBookPage(basePage);
    }

    /**
     * 读者规则查询
     *
     * @return R<List < BookRule>>
     */
    @GetMapping("get_rulelist")
    @ApiOperation("读者规则查询")
    public R<List<BookRule>> getRuleList() {
        return bookRuleService.getRuleList();
    }

    /**
     * 查询公告信息
     *
     * @return R<List < Notice>>
     */
    @GetMapping("get_noticelist")
    @ApiOperation("查询公告信息")
    public R<List<Notice>> getNoticeList() {
        return noticeService.getNoticeList();
    }

    /**
     * Rest接受参数 查询个人用户userId
     *
     * @param userId 用户id
     * @return R<Users>
     */
    @GetMapping("get_information/{userId}")
    @ApiOperation("查询个人用户")
    public R<Users> getUserByUserId(@PathVariable("userId") Integer userId) {
        return usersService.getUserByUserId(userId);
    }

    /**
     * 修改密码
     *
     * @return R
     */
    @PostMapping("update_password")
    @ApiOperation("修改密码")
    public R<String> updatePassword(@RequestBody Users users) {
        return usersService.updatePassword(users);
    }

    /**
     * 借阅信息查询 根据用户id，条件及其内容
     *
     * @param basePage 用于接受分页传参和用户id
     * @return R<Page < BooksBorrow>>
     */
    @PostMapping("get_bookborrow")
    @ApiOperation("借阅信息查询")
    public R<Page<BooksBorrow>> getBookBorrowPage(@RequestBody BasePage basePage) {
        return booksBorrowService.getBookBorrowPage(basePage);
    }

    /**
     * 查询违章信息(借阅证)
     *
     * @param basePage 获取前端的分页参数，条件和内容，借阅证
     * @return R<Page < ViolationDTO>>
     */
    @PostMapping("get_violation")
    @ApiOperation("查询违章信息")
    public R<Page<ViolationDTO>> getViolationListByPage(@RequestBody BasePage basePage) {
        return violationService.getViolationListByPage(basePage);
    }

    /**
     * 获取弹幕列表
     *
     * @return R<Comment>
     */
    @GetMapping("get_commentlist")
    @ApiOperation("获取弹幕列表")
    public R<List<CommentDTO>> getCommentList() {
        return commentService.getCommentList();

    }

    /**
     * 添加弹幕
     *
     * @return R
     */
    @PostMapping("add_comment")
    @ApiOperation("添加弹幕")
    public R<String> addComment(@RequestBody CommentDTO commentDTO, @RequestHeader("Authorization") String token) {
        String userName = jwtKit.getUsernameFromToken(token);
        commentDTO.setUserName(extractUsername(userName));
        return commentService.addComment(commentDTO);
    }

    /**
     * 调用AI模型，获取数据库中有的，并且推荐图书给用户
     * @param aiIntelligent AI实体类
     * @return R<String>
     */
    @PostMapping("ai_intelligent")
    @ApiOperation("推荐图书")
    public R<String> aiRecommend(@RequestBody AiIntelligent aiIntelligent){
        return aiIntelligentService.getGenResult(aiIntelligent);
    }

    /**
     * 根据用户ID 获取该用户和AI聊天的最近的五条消息
     * @param userId 用户id
     * @return R<List<AiIntelligent>>
     */
    @GetMapping("ai_list_information/{userId}")
    @ApiOperation("获取该用户和AI聊天的最近的五条消息")
    public R<List<AiIntelligent>> getAiInformationByUserId(@PathVariable("userId") Long userId){
        return aiIntelligentService.getAiInformationByUserId(userId);
    }

    /**
     * 回复评论
     *
     * @param replyDTO 带 parentId 的 ReplyDTO 对象
     * @param token    请求头中的 token
     * @return R<String>
     */
    @PostMapping("reply_comment")
    @ApiOperation("回复评论")
    public R<String> replyComment(@RequestBody ReplyDTO replyDTO, @RequestHeader("Authorization") String token) {
        String username = jwtKit.getUsernameFromToken(token);
//      截取里的username  Users(userId=1923, username=相思断红肠, password=da4c189f916ae0b5aeb59389df4f0df0, cardName=张三, cardNumber=18012345678, ruleNumber=188, status=1, createTime=2023-02-02 16:12:05, updateTime=2023-02-02 16:12:05)

        replyDTO.setUserName(extractUsername(username));
        return commentService.replyComment(replyDTO);
    }

    private   String extractUsername(String input) {
        // 正则表达式匹配 username= 后的内容，直到遇到逗号或右括号
        Pattern pattern = Pattern.compile("username=([^,\\)]+)");
        Matcher matcher = pattern.matcher(input);

        if (matcher.find()) {
            return matcher.group(1).trim(); // 返回匹配到的内容并去除两边空格
        }

        return null; // 没有找到返回 null
    }

    /**
     * 用户评分接口
     *
     * @param ratingDTO 包含 bookNumber 和 score
     * @param token     请求头中的 token
     * @return R<String>
     */
    @PostMapping("rate_book")
    @ApiOperation("用户给图书评分")
    public R<String> rateBook(@RequestBody RatingDTO ratingDTO, @RequestHeader("Authorization") String token) {
        String username = jwtKit.getUsernameFromToken(token);
        String cleanUsername = extractUsername(username);

        ratingDTO.setUsername(cleanUsername);

        return booksService.rateBook(ratingDTO);
    }



}
