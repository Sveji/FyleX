import './analysis.less'

const AnalysisBox = ({ text = "Here are some parts of your document that you might need to reconsider:", sentences = [] }) => {

    return (
        <div className="analysis-box">
            <div className="title-box">
                <h1>Analysis</h1>
            </div>

            <p className='text'>{text}</p>

            <div className="sentences-container">
                {
                    sentences && sentences.length > 0 &&
                    sentences.map((sentence, i) => (
                        <div key={i} className="sentence-box">
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