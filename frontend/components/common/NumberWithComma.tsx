import React from "react";

type NumberWithCommaProps = {
    value: number | string;
    locale?: string;
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