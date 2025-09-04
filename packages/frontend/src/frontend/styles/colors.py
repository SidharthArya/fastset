"""Color system variables - Softer, eye-friendly palette"""
from fasthtml.common import Style

# Softer color palette for better eye comfort
color_variables = Style("""
    :root {
        /* Primary Colors - Softer Teal */
        --primary: #5CBDB1;           /* Softer teal - Main brand color */
        --primary-hover: #4A9B91;    /* Darker teal for hover states */
        --primary-light: rgba(92, 189, 177, 0.08);  /* Very light teal for backgrounds */
        
        /* Secondary Colors - Muted Purple */
        --secondary: #8B6BB1;         /* Muted purple - Secondary brand color */
        --secondary-hover: #7A5A9A;  /* Darker purple for hover states */
        --secondary-light: rgba(139, 107, 177, 0.08);  /* Light purple for backgrounds */
        
        /* Tertiary Colors - Gentle Yellow-Green */
        --tertiary: #A8B56A;         /* Gentle yellow-green - Accent color */
        --tertiary-hover: #8F9B57;   /* Darker yellow-green for hover states */
        --tertiary-light: rgba(168, 181, 106, 0.08);  /* Light yellow-green for backgrounds */
        
        /* Accent Colors - Warm Orange */
        --accent: #C4896B;           /* Warm orange - Warning/accent color */
        --accent-hover: #A8735A;    /* Darker orange for hover states */
        --accent-light: rgba(196, 137, 107, 0.08);  /* Light orange for backgrounds */
        
        /* Text Colors - Softer, less harsh */
        --text-primary: #4A5553;     /* Softer dark green-gray - Primary text */
        --text-secondary: #6B6B7A;   /* Softer purple-gray - Secondary text */
        --text-muted: #8B9299;       /* Gentle muted gray - Tertiary text */
        --text-inverse: #ffffff;     /* White - Text on dark backgrounds */
        
        /* Background Colors - Warmer whites */
        --bg-primary: #fefefe;       /* Slightly off-white - Primary background */
        --bg-secondary: #f9fafb;     /* Very light warm gray - Secondary background */
        --bg-tertiary: #f4f6f7;      /* Light warm gray - Tertiary background */
        
        /* Border Colors - Gentler borders */
        --border-light: rgba(107, 107, 122, 0.15);     /* Very light border */
        --border-medium: rgba(107, 107, 122, 0.25);    /* Medium border */
        --border-dark: rgba(107, 107, 122, 0.4);       /* Dark border */
        
        /* Shadow Colors - Softer shadows */
        --shadow-light: rgba(74, 85, 83, 0.06);        /* Very light shadow */
        --shadow-medium: rgba(74, 85, 83, 0.1);        /* Medium shadow */
        --shadow-dark: rgba(74, 85, 83, 0.18);         /* Dark shadow */
        
        /* Gradients (2 colors only) - Gentler transitions */
        --gradient-primary: linear-gradient(135deg, var(--primary), var(--secondary));
        --gradient-secondary: linear-gradient(135deg, var(--secondary), var(--primary));
        --gradient-background: linear-gradient(135deg, var(--primary), var(--secondary));
        --gradient-accent: linear-gradient(135deg, var(--tertiary), var(--accent));
    }

    /* Dark Theme */
    [data-theme="dark"] {
        /* Primary Colors - Dark theme variants */
        --primary: #4ECDC4;           /* Brighter teal for dark backgrounds */
        --primary-hover: #3BB5AC;    /* Darker teal for hover states */
        --primary-light: rgba(78, 205, 196, 0.12);  /* Light teal for dark backgrounds */
        
        /* Secondary Colors - Dark theme variants */
        --secondary: #A78BFA;         /* Brighter purple for dark backgrounds */
        --secondary-hover: #8B5CF6;  /* Darker purple for hover states */
        --secondary-light: rgba(167, 139, 250, 0.12);  /* Light purple for dark backgrounds */
        
        /* Tertiary Colors - Dark theme variants */
        --tertiary: #BEF264;         /* Brighter yellow-green for dark backgrounds */
        --tertiary-hover: #A3E635;   /* Darker yellow-green for hover states */
        --tertiary-light: rgba(190, 242, 100, 0.12);  /* Light yellow-green for dark backgrounds */
        
        /* Accent Colors - Dark theme variants */
        --accent: #FB923C;           /* Brighter orange for dark backgrounds */
        --accent-hover: #F97316;    /* Darker orange for hover states */
        --accent-light: rgba(251, 146, 60, 0.12);  /* Light orange for dark backgrounds */
        
        /* Text Colors - Dark theme */
        --text-primary: #F8FAFC;     /* Light gray - Primary text on dark */
        --text-secondary: #CBD5E1;   /* Medium gray - Secondary text on dark */
        --text-muted: #94A3B8;       /* Muted gray - Tertiary text on dark */
        --text-inverse: #1E293B;     /* Dark - Text on light backgrounds */
        
        /* Background Colors - Dark theme */
        --bg-primary: #1E293B;       /* Dark slate - Primary background */
        --bg-secondary: #334155;     /* Medium slate - Secondary background */
        --bg-tertiary: #475569;      /* Light slate - Tertiary background */
        
        /* Border Colors - Dark theme */
        --border-light: rgba(203, 213, 225, 0.15);     /* Light border on dark */
        --border-medium: rgba(203, 213, 225, 0.25);    /* Medium border on dark */
        --border-dark: rgba(203, 213, 225, 0.4);       /* Dark border on dark */
        
        /* Shadow Colors - Dark theme */
        --shadow-light: rgba(0, 0, 0, 0.2);            /* Light shadow on dark */
        --shadow-medium: rgba(0, 0, 0, 0.3);           /* Medium shadow on dark */
        --shadow-dark: rgba(0, 0, 0, 0.5);             /* Dark shadow on dark */
        
        /* Gradients - Dark theme */
        --gradient-primary: linear-gradient(135deg, var(--primary), var(--secondary));
        --gradient-secondary: linear-gradient(135deg, var(--secondary), var(--primary));
        --gradient-background: linear-gradient(135deg, #1E293B, #334155);
        --gradient-accent: linear-gradient(135deg, var(--tertiary), var(--accent));
    }
""")