import './analysis.less'

const AnalysisBox = ({ text = "Here are some parts of your document that you might need to reconsider:", sentences = [] }) => {
    // const sentences = [
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     },
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     },
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     },
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     },
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     },
    //     {
    //         sentence: "Eleifend eu vulputate eleifend metus sit in scelerisque. Molestie in in auctor leo. Diam eget at eu porttitor quam convallis nibh morbi etiam.",
    //         analysis: "This part is something you might need to reconsider, since it targets your personal finances and not the company’s ones. This means that if you perhaps one day go into debt, they can take your personal possesions too. Try to change it."
    //     }
    // ]

    return (
        <div className="analysis-box">
            <div className="title-box">
                <h1>Analysis</h1>
            </div>

            <p className='text'>{text}</p>

            <div className="sentences-container">
                {
                    sentences && sentences.length > 0 &&
                    sentences.map(sentence => (
                        <div className="sentence-box">
                            <p className="sentence">{sentence}</p>
                            {/* <p className="analysis">{sentence.analysis}</p> */}
                        </div>
                    ))
                }
            </div>
        </div>
    )
}

export default AnalysisBox