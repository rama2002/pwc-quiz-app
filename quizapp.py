import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage

OPENAI_API_KEY = "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"

def main():
    st.title("AI Quiz Generator")
    topic = st.text_input("Enter your preferred quiz topic:")
    num_questions = st.number_input("Enter the number of questions:", min_value=1, value=None, step=1)
    generatequiz = st.button("Generate Quiz")
    
    if topic and num_questions:
        if generatequiz:
            quiz = generate_quiz(topic, num_questions)
            st.session_state.quiz = quiz
        if 'quiz' in st.session_state:
            quiz = st.session_state.quiz
            with st.form("quiz_form"):
                user_answers = []
                for i, qna in enumerate(quiz, start=1):
                    st.write(qna['question'])
                    selected_option = st.radio(f"Select answer for Q{i}:", qna['options'], key=f"question_{i}")
                    user_answers.append(selected_option)
                submitted = st.form_submit_button("Submit Answers")
                if submitted:
                    st.divider()
                    total_questions = len(user_answers)
                    correct_questions = 0
                    for i in range(total_questions):
                        answer = quiz[i]['correct_answer']
                        st.text(f"For {quiz[i]['question']}")
                        st.text(f"The correct answer is: {answer}")
                        st.text(f"You answered: {user_answers[i]}")
                        if answer == user_answers[i]:
                            st.text("You answered correctly")
                            correct_questions += 1
                        else:
                            st.text("You answered wrong")
                        st.divider()
                    result = correct_questions / total_questions * 100
                    st.text("You recieved a score of %d / 100" % result)

    else:
        st.warning("Please enter a quiz topic.")
    
def generate_quiz(topic, num_questions):
    quiz = []
    while len(quiz) < num_questions:
        chat_model  = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4")
        prompt = f"Generate a multiple-choice quiz question with answer and choices in uppercase alphabetical list of 4 items maximum on the topic: {topic}."
        messages = [AIMessage(content=prompt)]
        try:
            result = chat_model.invoke(messages).content.replace('\n\n', '\n').strip()
            print(result)
            question_text = ""
            if "A." in result:
              question_text = result.split('A.')[0].strip()
            else:
              question_text = result.split('A)')[0].strip()
            correct_answer = result.split("Answer: ")[1].strip()
            answer_options = result.split("Answer: ")[0].strip().split(question_text)[1].strip().split("\n")
            quiz.append({
                'question': question_text,
                'options': answer_options,
                'correct_answer': correct_answer
            })
        except:
            print("error")
            continue

    return quiz
    
if __name__ == "__main__":
    main()