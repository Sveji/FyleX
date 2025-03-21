import { Link } from "react-router-dom"
import './account.less'
import { useContext, useEffect } from "react"
import { DataContext } from "../../context/DataContext"
import { GoogleLogin } from '@react-oauth/google'

const AccountForm = ({ handleSubmit, title = "", text = "", inputs = [], btn = "", link, error = null, forgotPass = false }) => {
    // Gets global data from the context
    const { access, navigate } = useContext(DataContext)



    // Checks if the user is logged in
    useEffect(() => {
        if(access) navigate('/')
    }, [access])



    const handleGoogleLoginSuccess = async (credentialResponse) => {
        const token = credentialResponse.credential;
        const decodedToken = parseJwt(token);

        const response = await crud({
            method: 'post',
            url: '/google-login/',
            body: {
                token,
                email: decodedToken.email,
            },
        });

        if (response.status === 200) {
            localStorage.setItem('access', response.data.access);
            setAccess(response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            setRefresh(response.data.refresh);
            navigate('/dashboard');
        } else {
            setError('Google Login failed');
        }
    };

    const handleGoogleLoginFailure = () => {
        setError('Google Login failed');
    };



    return (
        <div>
            <div className="text-box">
                <h1>{title}</h1>
                <p>{text}</p>
                {error && <p className="error">{error}</p>}
            </div>

            <form className="account-form" onSubmit={(e) => handleSubmit(e)}>
                <div className="input-box">
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
                </div>
                {
                    forgotPass &&
                    <Link to='/forgot-pass' className="forgot">Forgot password?</Link>
                }

                <button className="btn" type='submit'>{btn}</button>
            </form>

            <div className="or-box">
                <div className="line"></div>
                <p>or</p>
                <div className="line"></div>
            </div>

            <GoogleLogin
                onSuccess={handleGoogleLoginSuccess}
                onError={handleGoogleLoginFailure}
            />

            <div className="redirect-text">
                <p>{link.text}</p>
                <Link className="link" to={link.route}><p className="bold">{link.label}</p></Link>
            </div>
        </div>
    )
}

export default AccountForm