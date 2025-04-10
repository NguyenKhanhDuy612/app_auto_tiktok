"use client";

import { useState } from "react";
import View from "@/components/TiktokSidebar/View";
import Follow from "@/components/TiktokSidebar/Follow";
import Heart from "@/components/TiktokSidebar/Heart";
import Like from "@/components/TiktokSidebar/Like";

function Tiktok() {
  const [activeComponent, setActiveComponent] = useState("view"); // Trạng thái mặc định là "view"
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // Trạng thái mở/đóng dropdown

  const renderComponent = () => {
    switch (activeComponent) {
      case "view":
        return <View />;
      case "like":
        return <Like />;
      case "follow":
        return <Follow />;
      case "heart":
        return <Heart />;
      default:
        return <View />;
    }
  };

  return (
    <>
      <div className="flex h-screen">
        {/* Sidebar */}
        <aside className="w-64 bg-gray-800 text-white flex flex-col">
          <nav className="flex-1">
            <ul className="space-y-2 p-4">
              {/* Dropdown Tiktok */}
              <li>
                <div
                  onClick={() => setIsDropdownOpen(!isDropdownOpen)} // Toggle trạng thái dropdown
                  className="cursor-pointer font-semibold hover:text-blue-400 flex justify-between items-center"
                >
                  TIKTOK
                  <span>{isDropdownOpen ? "▲" : "▼"}</span> {/* Biểu tượng mở/đóng */}
                </div>
                {isDropdownOpen && ( // Hiển thị dropdown nếu trạng thái mở
                  <ul className="pl-4 space-y-1 mt-2">
                    <li
                      onClick={() => setActiveComponent("view")}
                      className="cursor-pointer hover:text-blue-400"
                    >
                      Tăng mắt live Tiktok
                    </li>
                    <li
                      onClick={() => setActiveComponent("follow")}
                      className="cursor-pointer hover:text-blue-400"
                    >
                      Tăng follow Tiktok
                    </li>
                    <li
                      onClick={() => setActiveComponent("heart")}
                      className="cursor-pointer hover:text-blue-400"
                    >
                      Tăng tim Tiktok
                    </li>
                    <li
                      onClick={() => setActiveComponent("like")}
                      className="cursor-pointer hover:text-blue-400"
                    >
                      Tăng like Tiktok
                    </li>
                  </ul>
                )}
              </li>
            </ul>
          </nav>
          <footer className="p-4"></footer>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8 bg-white">
          <h1 className="text-xl font-bold mb-4">Dịch vụ Tiktok</h1>
          {renderComponent()} {/* Hiển thị component dựa trên trạng thái */}
        </main>
      </div>
    </>
  );
}

export default Tiktok;