import { Link } from "react-router-dom"
import './account.less'
import { useContext, useEffect } from "react"
import { DataContext } from "../../context/DataContext"

const AccountForm = ({ handleSubmit, title = "", text = "", inputs = [], btn = "", link, error = null }) => {
    // Gets global data from the context
    const { access, navigate } = useContext(DataContext)



    // Checks if the user is logged in
    useEffect(() => {
        if(access) navigate('/')
    }, [access])



    return (
        <div>
            <div className="text-box">
                <h1>{title}</h1>
                <p>{text}</p>
                {error && <p className="error">{error}</p>}
            </div>

            <form className="account-form" onSubmit={(e) => handleSubmit(e)}>
                {
                    inputs.map((inputField, i) =>(
                        <input
                            key={i}
                            type={inputField.type}
                            value={inputField.value}
                            onChange={(e) => inputField.setValue(e.target.value)}
                            placeholder={inputField.placeholder}
                        />
                    ))
                }
                <button className="btn" type='submit'>{btn}</button>
            </form>

            <div className="redirect-text">
                <p>{link.text}</p>
                <Link className="link" to={link.route}><p className="bold">{link.label}</p></Link>
            </div>
        </div>
    )
}

export default AccountForm