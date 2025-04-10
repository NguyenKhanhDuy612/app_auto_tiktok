

export const Header = () => (
    <header className="flex items-center justify-between p-4 bg-gray-800 text-white">
      
        <div className="flex items-center">
            <img
                src="/logo.png"
                alt="Logo"
                className="h-8 w-8 mr-2" />
            <span className="text-lg font-bold">App Buff TikTok</span>
        </div>
    </header>
);

  export default Header;