import NavBar_module from './NavBar.module.scss';
import { OnOffBtnCmp } from './on-off-btn-cmp/on-off-btn-cmp';
import { TTSOnOff } from './TTTSOnOff/TTSOnOff';

// Define an interface for the component props
interface NavBarProps {
    stt: boolean;
    tts: boolean;
}

// Apply the interface to the component function
const NavBar: React.FC<NavBarProps> = ({ stt, tts }) => {
    return (
        <div className={NavBar_module.NavBarStyle}>
            <div className={NavBar_module.MainButtonsNavBar}>
                <button className={NavBar_module.HomeBut}>Home</button>
                <button className={NavBar_module.PWBut}>PW</button>
                <button className={NavBar_module.CalendarBut}>Calendar</button>
            </div>
            <div className={NavBar_module.middleSec}>
                <TTSOnOff tts={tts} />
                <OnOffBtnCmp stt={stt} />
            </div>
            <div color="blue" className={NavBar_module.RightNavBar}>
                <button className={NavBar_module.settingsButton}>Settings</button>
            </div>
        </div>
    );
}

export default NavBar;
