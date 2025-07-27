/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, onMounted, useRef } from "@odoo/owl";
import {loadJS} from '@web/core/assets';
import { useService } from "@web/core/utils/hooks";

export class FarmerDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.chartRef = useRef('chartCanvas');
        this.lineChart= useRef('lineCanvas');

        this.state = useState({
            revenue_total: 0,
            expense_total: 0,
        });

        onWillStart(async () => {
            await this.fetchRevenueTotal();
            await this.fetchExpenseTotal();

            try{
                await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
            } catch (error) {
                console.error("Error loading Chart.js:", error);
            }
        });

        // Render Chart when component is mounted
        onMounted(() => {
            this.renderChart();
            this.renderLineChart();
        })
    }


    // Fetch Total Revenue Data
    async fetchRevenueTotal() {
        try {
            const result = await this.orm.call("account.move", "search_read", [
                [
                    ["move_type", "=", "out_invoice"],
                    ["payment_state", "in", ["paid", "in_payment"]],
                    ["state", "=", "posted"],
                ],
                ["amount_total_signed"]
            ]);
            this.state.revenue_total = result.reduce((total, invoice) => total + invoice.amount_total_signed, 0);
            console.log("Revenue Total", this.state.revenue_total);
        } catch (error) {
            console.error("Error fetching revenue total:", error);
            this.state.revenue_total = 0;
        }
    }

    // Fetch Total Expense Data
    async fetchExpenseTotal() {
        try {
            const result = await this.orm.call("account.move", "search_read", [
                [
                    ["move_type", "=", "in_invoice"],
                    ["payment_state", "in", ["paid", "in_payment"]],
                    ["state", "=", "posted"],
                ],
                ["amount_total_signed"]
            ]);
            this.state.expense_total = result.reduce((total, invoice) => total + invoice.amount_total_signed, 0);
            console.log("Expense Total", this.state.expense_total);
        } catch (error) {
            console.error("Error fetching expense total:", error);
            this.state.expense_total = 0;
        }
    }

    // Render Chart
    renderChart() {
        if (!window.Chart) {
            console.error("Chart.js not loaded yet!");
            return;
        }

        const canvas = this.chartRef.el; // Get the canvas element safely
        if (!canvas) {
            console.error("Canvas element not found!");
            return;
        }

        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "August", "September", "October", "November", "December"],
                datasets: [
                    {
                    label: "Revenue",
                    data: [100, 200, 150, 300, 250, 110, 180, 170, 240, 102, 451, 124],
                    backgroundColor: "#137e2e",  // Using a single green color for all bars
                },
                {
                    label: "Expense",
                    data: [100, 200, 150, 300, 250, 110, 180, 170, 240, 102, 451, 124],
                    backgroundColor: "#c64433",  // Using a single red color for all bars
                }
            ]
            },
            options: {
                responsive: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }


    // Render Line Chart
    renderLineChart() {
        if (!window.Chart) {
            console.error("Chart.js not loaded yet!");
            return;
        }

        const canvas = this.lineChart.el; // Get the canvas element safely
        if (!canvas) {
            console.error("Canvas element not found!");
            return;
        }

        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "August", "September", "October", "November", "December"],
                datasets: [
                        {
                        label: "Mortality Rate",
                        data: [100, 200, 150, 300, 250, 110, 180, 170, 240, 102, 451, 124],
                        backgroundColor: "#131722",  // Using a single green color for all bars
                    },
                ]
            },
            options: {
                responsive: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
}

// Set the template
FarmerDashboard.template = "farmer_dashboard";

// Register the action
registry.category("actions").add("farmer_dashboard", FarmerDashboard);