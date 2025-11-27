import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

DSA_QUESTIONS = {
    "Arrays": [
        {"title": "Two Sum", "difficulty": "Easy", "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.", "hint": "Use a hash map to store complements"},
        {"title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "description": "Find the maximum profit from buying and selling stock once.", "hint": "Track minimum price seen so far"},
        {"title": "Container With Most Water", "difficulty": "Medium", "description": "Find two lines that together with x-axis form a container with most water.", "hint": "Use two pointers approach"},
        {"title": "3Sum", "difficulty": "Medium", "description": "Find all unique triplets in array that sum to zero.", "hint": "Sort array first, then use two pointers"},
        {"title": "Trapping Rain Water", "difficulty": "Hard", "description": "Calculate how much rain water can be trapped between elevation bars.", "hint": "Track max height from left and right"},
    ],
    "Linked Lists": [
        {"title": "Reverse Linked List", "difficulty": "Easy", "description": "Reverse a singly linked list.", "hint": "Use three pointers: prev, current, next"},
        {"title": "Detect Cycle", "difficulty": "Easy", "description": "Detect if a linked list has a cycle.", "hint": "Floyd's cycle detection (tortoise and hare)"},
        {"title": "Merge Two Sorted Lists", "difficulty": "Easy", "description": "Merge two sorted linked lists into one sorted list.", "hint": "Use dummy node and two pointers"},
        {"title": "Remove Nth Node From End", "difficulty": "Medium", "description": "Remove the nth node from the end of list.", "hint": "Use two pointers with n gap between them"},
        {"title": "Copy List with Random Pointer", "difficulty": "Medium", "description": "Deep copy a linked list with random pointers.", "hint": "Use hash map or interweaving approach"},
    ],
    "Trees": [
        {"title": "Maximum Depth of Binary Tree", "difficulty": "Easy", "description": "Find the maximum depth of a binary tree.", "hint": "Use recursion or BFS"},
        {"title": "Invert Binary Tree", "difficulty": "Easy", "description": "Invert a binary tree (mirror it).", "hint": "Swap left and right children recursively"},
        {"title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "description": "Return level order traversal of nodes' values.", "hint": "Use queue for BFS"},
        {"title": "Validate Binary Search Tree", "difficulty": "Medium", "description": "Check if a tree is a valid BST.", "hint": "Track min and max values allowed"},
        {"title": "Serialize and Deserialize Binary Tree", "difficulty": "Hard", "description": "Design algorithm to serialize/deserialize binary tree.", "hint": "Use preorder traversal with markers"},
    ],
    "Graphs": [
        {"title": "Number of Islands", "difficulty": "Medium", "description": "Count number of islands in 2D grid.", "hint": "Use DFS or BFS to mark connected components"},
        {"title": "Clone Graph", "difficulty": "Medium", "description": "Deep copy an undirected graph.", "hint": "Use hash map and DFS/BFS"},
        {"title": "Course Schedule", "difficulty": "Medium", "description": "Check if you can finish all courses given prerequisites.", "hint": "Detect cycle in directed graph"},
        {"title": "Word Ladder", "difficulty": "Hard", "description": "Find shortest transformation sequence from beginWord to endWord.", "hint": "Use BFS with word variations"},
        {"title": "Alien Dictionary", "difficulty": "Hard", "description": "Derive order of characters in alien language.", "hint": "Topological sort"},
    ],
    "Dynamic Programming": [
        {"title": "Climbing Stairs", "difficulty": "Easy", "description": "Count ways to climb n stairs (1 or 2 steps at a time).", "hint": "Fibonacci sequence"},
        {"title": "House Robber", "difficulty": "Medium", "description": "Rob houses to maximize money without robbing adjacent houses.", "hint": "dp[i] = max(rob i + dp[i-2], skip i = dp[i-1])"},
        {"title": "Longest Increasing Subsequence", "difficulty": "Medium", "description": "Find length of longest increasing subsequence.", "hint": "DP or binary search approach"},
        {"title": "Coin Change", "difficulty": "Medium", "description": "Find minimum coins needed to make amount.", "hint": "Bottom-up DP with amount as state"},
        {"title": "Edit Distance", "difficulty": "Hard", "description": "Find minimum operations to convert word1 to word2.", "hint": "2D DP table comparing characters"},
    ],
    "Strings": [
        {"title": "Valid Anagram", "difficulty": "Easy", "description": "Check if two strings are anagrams.", "hint": "Use character frequency map"},
        {"title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "description": "Find length of longest substring without repeating chars.", "hint": "Sliding window with hash set"},
        {"title": "Longest Palindromic Substring", "difficulty": "Medium", "description": "Find the longest palindromic substring.", "hint": "Expand around center"},
        {"title": "Group Anagrams", "difficulty": "Medium", "description": "Group anagrams together from array of strings.", "hint": "Use sorted string as key"},
        {"title": "Minimum Window Substring", "difficulty": "Hard", "description": "Find minimum window in s containing all characters of t.", "hint": "Sliding window with two pointers"},
    ],
    "Stack & Queue": [
        {"title": "Valid Parentheses", "difficulty": "Easy", "description": "Check if string has valid parentheses.", "hint": "Use stack to match opening/closing brackets"},
        {"title": "Min Stack", "difficulty": "Medium", "description": "Design stack with push, pop, top, and getMin in O(1).", "hint": "Use auxiliary stack to track minimums"},
        {"title": "Daily Temperatures", "difficulty": "Medium", "description": "Find how many days until warmer temperature.", "hint": "Monotonic stack"},
        {"title": "Implement Queue using Stacks", "difficulty": "Easy", "description": "Implement queue using only two stacks.", "hint": "Use one stack for enqueue, one for dequeue"},
        {"title": "Largest Rectangle in Histogram", "difficulty": "Hard", "description": "Find largest rectangle area in histogram.", "hint": "Stack to track indices of bars"},
    ],
    "Heap": [
        {"title": "Kth Largest Element", "difficulty": "Medium", "description": "Find kth largest element in unsorted array.", "hint": "Use min heap of size k"},
        {"title": "Top K Frequent Elements", "difficulty": "Medium", "description": "Find k most frequent elements.", "hint": "Use heap or bucket sort"},
        {"title": "Merge K Sorted Lists", "difficulty": "Hard", "description": "Merge k sorted linked lists into one.", "hint": "Use min heap with k elements"},
        {"title": "Find Median from Data Stream", "difficulty": "Hard", "description": "Design data structure to find median from stream.", "hint": "Two heaps: max heap for lower half, min heap for upper"},
        {"title": "Task Scheduler", "difficulty": "Medium", "description": "Schedule tasks with cooldown period.", "hint": "Use heap with frequency counts"},
    ],
    "Binary Search": [
        {"title": "Binary Search", "difficulty": "Easy", "description": "Implement binary search on sorted array.", "hint": "mid = (left + right) // 2"},
        {"title": "Search in Rotated Sorted Array", "difficulty": "Medium", "description": "Search target in rotated sorted array.", "hint": "Find which half is sorted first"},
        {"title": "Find Minimum in Rotated Sorted Array", "difficulty": "Medium", "description": "Find minimum element in rotated array.", "hint": "Compare mid with right boundary"},
        {"title": "Search a 2D Matrix", "difficulty": "Medium", "description": "Search target in 2D matrix with sorted properties.", "hint": "Treat as 1D sorted array"},
        {"title": "Median of Two Sorted Arrays", "difficulty": "Hard", "description": "Find median of two sorted arrays in O(log(m+n)).", "hint": "Binary search on partition"},
    ],
    "Backtracking": [
        {"title": "Subsets", "difficulty": "Medium", "description": "Generate all possible subsets of a set.", "hint": "Include/exclude each element recursively"},
        {"title": "Permutations", "difficulty": "Medium", "description": "Generate all permutations of distinct integers.", "hint": "Backtrack with swap or used array"},
        {"title": "Combination Sum", "difficulty": "Medium", "description": "Find all unique combinations that sum to target.", "hint": "Backtrack with remaining sum"},
        {"title": "Word Search", "difficulty": "Medium", "description": "Check if word exists in 2D board.", "hint": "DFS with backtracking, mark visited cells"},
        {"title": "N-Queens", "difficulty": "Hard", "description": "Place n queens on n×n board so none attack each other.", "hint": "Track columns and diagonals"},
    ],
}

user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"streak": 0, "solved": [], "last_date": None}
    
    welcome_text = """
*Welcome to DSA Question of the Day Bot!*

Get a daily DSA question to sharpen your problem-solving skills!

*Commands:*
/qotd - Get today's question
/random - Get a random question
/topics - Browse questions by topic
/stats - View your progress
/hint - Get a hint for current question
/solution - Mark question as solved
/help - Show this help message

Let's start coding! 
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def qotd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().date()
    user_id = update.effective_user.id
    
    if user_id not in user_progress:
        user_progress[user_id] = {"streak": 0, "solved": [], "last_date": None}
    random.seed(today.toordinal())
    topic = random.choice(list(DSA_QUESTIONS.keys()))
    question = random.choice(DSA_QUESTIONS[topic])
    
    context.user_data['current_question'] = question
    context.user_data['current_topic'] = topic
    
    difficulty_tags= {"Easy": "E", "Medium": "M", "Hard": "H"}
    
    message = f"""
    *Question of the Day* - {today.strftime('%B %d, %Y')}

*Topic:* {topic}
{difficulty_tags[question['difficulty']]} *Difficulty:* {question['difficulty']}

*{question['title']}*

{question['description']}

Good luck! 

Use /hint for a hint or /solution when you've solved it!
    """
    
    keyboard = [
        [InlineKeyboardButton(" Get Hint", callback_data="hint")],
        [InlineKeyboardButton(" Mark as Solved", callback_data="solved")],
        [InlineKeyboardButton(" Different Question", callback_data="random")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def random_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = random.choice(list(DSA_QUESTIONS.keys()))
    question = random.choice(DSA_QUESTIONS[topic])
    
    context.user_data['current_question'] = question
    context.user_data['current_topic'] = topic
    
    difficulty_tags  = {"Easy": "E", "Medium": "M", "Hard": "H"}
    
    message = f"""
*Random Question*

  *Topic:* {topic}
{difficulty_tags[question['difficulty']]} *Difficulty:* {question['difficulty']}

*{question['title']}*

{question['description']}

Use /hint for a hint or /solution when you've solved it!
    """
    
    keyboard = [
        [InlineKeyboardButton("Get Hint", callback_data="hint")],
        [InlineKeyboardButton("Mark as Solved", callback_data="solved")],
        [InlineKeyboardButton("Another Random", callback_data="random")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for topic in DSA_QUESTIONS.keys():
        count = len(DSA_QUESTIONS[topic])
        keyboard.append([InlineKeyboardButton(f"{topic} ({count} questions)", callback_data=f"topic_{topic}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("*Choose a Topic:*", parse_mode='Markdown', reply_markup=reply_markup)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in user_progress:
        user_progress[user_id] = {"streak": 0, "solved": [], "last_date": None}
    
    progress = user_progress[user_id]
    total_questions = sum(len(questions) for questions in DSA_QUESTIONS.values())
    solved_count = len(progress['solved'])
    
    stats_text = f"""
  *Your Progress*

  Questions Solved: {solved_count}/{total_questions}
  Current Streak: {progress['streak']} days
  Completion: {(solved_count/total_questions*100):.1f}%


    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = context.user_data.get('current_question')
    
    if not question:
        await update.message.reply_text("No active question! Use /qotd or /random first.")
        return
    
    hint_text = f"*Hint:* {question['hint']}"
    await update.message.reply_text(hint_text, parse_mode='Markdown')

async def solution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    question = context.user_data.get('current_question')
    
    if not question:
        await update.message.reply_text("No active question! Use /qotd or /random first.")
        return
    
    if user_id not in user_progress:
        user_progress[user_id] = {"streak": 0, "solved": [], "last_date": None}
    
    question_id = question['title']
    if question_id not in user_progress[user_id]['solved']:
        user_progress[user_id]['solved'].append(question_id)
        
        today = datetime.now().date()
        last_date = user_progress[user_id]['last_date']
        
        if last_date:
            days_diff = (today - last_date).days
            if days_diff == 1:
                user_progress[user_id]['streak'] += 1
            elif days_diff > 1:
                user_progress[user_id]['streak'] = 1
        else:
            user_progress[user_id]['streak'] = 1
        
        user_progress[user_id]['last_date'] = today
        
        congrats_text = f"""
*Congratulations!*

You've solved: *{question['title']}*
  Current Streak: {user_progress[user_id]['streak']} days

Keep up the great work! 
        """
    else:
        congrats_text = "You've already solved this question! Try /random for a new challenge."
    
    await update.message.reply_text(congrats_text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "hint":
        question = context.user_data.get('current_question')
        if question:
            await query.message.reply_text(f"*Hint:* {question['hint']}", parse_mode='Markdown')
        else:
            await query.message.reply_text("No active question!")
    
    elif query.data == "solved":
        user_id = update.effective_user.id
        question = context.user_data.get('current_question')
        
        if question:
            if user_id not in user_progress:
                user_progress[user_id] = {"streak": 0, "solved": [], "last_date": None}
            
            question_id = question['title']
            if question_id not in user_progress[user_id]['solved']:
                user_progress[user_id]['solved'].append(question_id)
                
                today = datetime.now().date()
                last_date = user_progress[user_id]['last_date']
                
                if last_date:
                    days_diff = (today - last_date).days
                    if days_diff == 1:
                        user_progress[user_id]['streak'] += 1
                    elif days_diff > 1:
                        user_progress[user_id]['streak'] = 1
                else:
                    user_progress[user_id]['streak'] = 1
                
                user_progress[user_id]['last_date'] = today
                
                await query.message.reply_text(
                    f"reat job! Streak: {user_progress[user_id]['streak']} days",
                    parse_mode='Markdown'
                )
            else:
                await query.message.reply_text("Already marked as solved!")
    
    elif query.data == "random":
        await random_question(update, context)
    
    elif query.data.startswith("topic_"):
        topic = query.data.replace("topic_", "")
        question = random.choice(DSA_QUESTIONS[topic])
        
        context.user_data['current_question'] = question
        context.user_data['current_topic'] = topic
        
        difficulty_tags = {"Easy": "E", "Medium": "M", "Hard" : "H"}
        
        message = f"""
    *Topic:* {topic}
{difficulty_tags[question['difficulty']]} *Difficulty:* {question['difficulty']}

*{question['title']}*

{question['description']}
        """
        
        keyboard = [
            [InlineKeyboardButton("Get Hint", callback_data="hint")],
            [InlineKeyboardButton("Mark as Solved", callback_data="solved")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8341451111:AAFSFVQ8Ax_wY_mc_UakFy-qea3OHP5POTs")
    
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Please set TELEGRAM_BOT_TOKEN environment variable!")
        return
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("qotd", qotd))
    application.add_handler(CommandHandler("random", random_question))
    application.add_handler(CommandHandler("topics", topics))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("hint", hint))
    application.add_handler(CommandHandler("solution", solution))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is running")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()