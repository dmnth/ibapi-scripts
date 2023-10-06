/* Copyright (C) 2023 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 * and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable. */

#include "StdAfx.h"
#include "Utils.h"

bool Utils::isPegBenchOrder(std::string orderType) {
    return orderType == "PEG BENCH" || orderType == "PEGBENCH";
}

bool Utils::isPegMidOrder(std::string orderType) {
    return orderType == "PEG MID" || orderType == "PEGMID";
}

bool Utils::isPegBestOrder(std::string orderType) {
    return orderType == "PEG BEST" || orderType == "PEGBEST";
}
