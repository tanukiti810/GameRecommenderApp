import React from "react";

type NumberWithCommaProps = {
    value: number | string; // 数値または数値文字列
    locale?: string;        // ロケール（例: "ja-JP", "en-US"）
};

const NumberWithComma: React.FC<NumberWithCommaProps> = ({
    value,
    locale = "ja-JP",
}) => {
    const num = Number(value);
    if (isNaN(num)) {
        console.error(`Invalid number: ${value}`);
        return <span>NaN</span>;
    }

    const formatted = new Intl.NumberFormat(locale).format(num);

    return <span>{formatted}</span>;
};

export default NumberWithComma;